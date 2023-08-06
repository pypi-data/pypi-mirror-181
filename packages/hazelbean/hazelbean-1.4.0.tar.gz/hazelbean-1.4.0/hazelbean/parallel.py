import rioxarray
import dask.array as da


def parallel_rasterstack_to_raster_compute(input_paths, op, output_path, n_workers=None, memory_limit=None):
    # input_paths can be a string path or a list of string paths
    # op is a function to be computed in parallel chunks. it must have as many inputs as the number of input_paths. op must return an array
    # output_path is where the tiled set of op arrays is saved.

    from dask.distributed import Client, LocalCluster, Lock


    if isinstance(input_paths, str):
        input_paths = [input_paths]

    if not isinstance(input_paths, list):
        raise NameError('dask_compute inputs must be a single path-string or a list of strings.')

    block_sizes = []
    for path in input_paths:
        if not hb.path_exists(path):
            raise NameError('dask_compute unable to find path: ' + str(path))
        block_sizes.append(hb.get_blocksize_from_path(path))

    # LEARNING POINT
    t_b = tuple([tuple(i) for i in block_sizes])

    if len(set(t_b)) > 1:
        critical_string = 'Paths given to dask_computer were not all saved in the same blocksize. This will have dramatic performance implications.'
        critical_string += '\n' + str(input_paths)
        critical_string += '\n' + str(block_sizes)
        L.critical(critical_string)

    if n_workers is None:
        print('num_cpu_available', str(multiprocessing.cpu_count()))
        n_workers = 8
        # n_workers = math.floor(multiprocessing.cpu_count() / 2) - 1 # For some reason, increasing this past like 8 even on a 128 core machine didn't help much. There must be some DASK magic utilizing all the cores even when n is low.
    if memory_limit is None:
        memory_limit = '8GB'
    threads_per_worker = 2 # Cause hyperthreading
    with LocalCluster(n_workers=n_workers, threads_per_worker=threads_per_worker, memory_limit=memory_limit) as cluster, Client(cluster) as client:
    # with LocalCluster() as cluster, Client(cluster) as client:
    # with LocalCluster(n_workers=math.floor(multiprocessing.cpu_count() / 2), threads_per_worker=2, memory_limit=str(math.floor(64 / (multiprocessing.cpu_count() + 1))) + 'GB') as cluster, Client(cluster) as client:

        L.info('Starting Local Cluster at http://localhost:8787/status')

        xds_list = []
        for input_path in input_paths:
            # xds = rioxarray.open_rasterio(input_path, chunks=(1, 512*4, 512*4), lock=False)
            # xds = rioxarray.open_rasterio(input_path, chunks=(1, 512*4, 512*4), lock=False)
            xds = rioxarray.open_rasterio(input_path, chunks='auto', lock=False)
            xds_list.append(xds)

        delayed_computation = op(*xds_list)
        delayed_computation.rio.to_raster(output_path, tiled=True, compress='DEFLATE', lock=Lock("rio", client=client))  # NOTE!!! MUCH FASTER WITH THIS. I think it's because it coordinates with the read to start the next thing asap.


def parallel_rasterstack_to_dict_compute(zones_path, values_path, output_path, n_workers=None, memory_limit=None):
    # input_paths can be a string path or a list of string paths
    # op is a function to be computed in parallel chunks. it must have as many inputs as the number of input_paths. op must return a dict
    # returns a dict that aggregates the tiled dicts.
    # optionally writes dict to csv at output_path

    from dask.distributed import Client, LocalCluster, Lock
    # import xrspatial

    input_paths = [zones_path, values_path]
    if isinstance(input_paths, str):
        input_paths = [input_paths]

    if not isinstance(input_paths, list):
        raise NameError('dask_compute inputs must be a single path-string or a list of strings.')

    block_sizes = []
    for path in input_paths:
        if not hb.path_exists(path):
            raise NameError('dask_compute unable to find path: ' + str(path))
        block_sizes.append(hb.get_blocksize_from_path(path))

    # LEARNING POINT
    t_b = tuple([tuple(i) for i in block_sizes])

    if len(set(t_b)) > 1:
        critical_string = 'Paths given to dask_computer were not all saved in the same blocksize. This will have dramatic performance implications.'
        critical_string += '\n' + str(input_paths)
        critical_string += '\n' + str(block_sizes)
        L.critical(critical_string)

    if n_workers is None:
        print('num_cpu_available', str(multiprocessing.cpu_count()))
        n_workers = 8
        # n_workers = math.floor(multiprocessing.cpu_count() / 2) - 1 # For some reason, increasing this past like 8 even on a 128 core machine didn't help much. There must be some DASK magic utilizing all the cores even when n is low.
    if memory_limit is None:
        memory_limit = '8GB'
    threads_per_worker = 2 # Cause hyperthreading
    def op(values_xds, zones_xds):
        values_array = values_xds.to_numpy()
        zones_array = zones_xds.to_numpy()
        unique_zone_ids = np.asarray(list(range(0, 255)))
        enumeration_classes = np.asarray(list(range(0, 255)))
        zones_ndv = 255
        values_ndv = -9999.0

        # dask_stats_df = xrspatial.zonal.stats(zones=zones_xds, values=values_xds)
        # print('dask_stats_df', dask_stats_df)
        # unique_zone_ids = xr
        # hb.zonal_statistics_flex()
        r = hb.zonal_stats_cythonized(zones_array,
                                         values_array,
                                         unique_zone_ids,
                                         zones_ndv,
                                         values_ndv,
                                         stats_to_retrieve = 'enumeration',
                                         reporting_frequency = 1000,
                                         enumeration_classes = enumeration_classes,
                                         # enumeration_classes = np.asarray([1], dtype=np.int64),
                                         )
        return r

    with LocalCluster(n_workers=n_workers, threads_per_worker=threads_per_worker, memory_limit=memory_limit) as cluster, Client(cluster) as client:
    # with LocalCluster() as cluster, Client(cluster) as client:
    # with LocalCluster(n_workers=math.floor(multiprocessing.cpu_count() / 2), threads_per_worker=2, memory_limit=str(math.floor(64 / (multiprocessing.cpu_count() + 1))) + 'GB') as cluster, Client(cluster) as client:

        L.info('Starting Local Cluster at http://localhost:8787/status')

        # xds_list = []
        # for input_path in input_paths:
        #     # xds = rioxarray.open_rasterio(input_path, chunks=(1, 512*4, 512*4), lock=False)
        #     # xds = rioxarray.open_rasterio(input_path, chunks=(1, 512*4, 512*4), lock=False)
        #     xds = rioxarray.open_rasterio(input_path, chunks='auto', lock=False)
        #     xds_list.append(xds)

        values_xds = rioxarray.open_rasterio(values_path, chunks=(1, 512*4, 512*4), lock=False)
        zones_xds = rioxarray.open_rasterio(zones_path, chunks=(1, 512*4, 512*4), lock=False)



        delayed_computation = op(values_xds, zones_xds)
        # delayed_computation = op(*xds_list)
        # delayed_computation.rio.to_raster(output_path, tiled=True, compress='DEFLATE', lock=Lock("rio", client=client))  # NOTE!!! MUCH FASTER WITH THIS. I think it's because it coordinates with the read to start the next thing asap.

#
# def parallel_zonal_statistics(zones_path, values_path, output_path, n_workers=None, memory_limit=None):
#     # input_paths can be a string path or a list of string paths
#     # op is a function to be computed in parallel chunks. it must have as many inputs as the number of input_paths. op must return a dict
#     # returns a dict that aggregates the tiled dicts.
#     # optionally writes dict to csv at output_path
#
#     from dask.distributed import Client, LocalCluster, Lock
#
#     enumeration_classes = list(range(0, 255))
#     enumeration = hb.zonal_stats_cythonized(
#         zones_array,
#         values_array,
#         unique_zone_ids_np,
#         zones_ndv=zones_ndv,
#         values_ndv=values_ndv,
#         stats_to_retrieve='enumeration',
#         enumeration_classes=np.asarray(enumeration_classes, dtype=np.int64),
#         # multiply_raster=np.asarray(multiply_raster, dtype=np.float64),
#     )
#
#     START HERE,m think about what is the sum
#
#
#     if isinstance(input_paths, str):
#         input_paths = [input_paths]
#
#     if not isinstance(input_paths, list):
#         raise NameError('dask_compute inputs must be a single path-string or a list of strings.')
#
#     block_sizes = []
#     for path in input_paths:
#         if not hb.path_exists(path):
#             raise NameError('dask_compute unable to find path: ' + str(path))
#         block_sizes.append(hb.get_blocksize_from_path(path))
#
#     # LEARNING POINT
#     t_b = tuple([tuple(i) for i in block_sizes])
#
#     if len(set(t_b)) > 1:
#         critical_string = 'Paths given to dask_computer were not all saved in the same blocksize. This will have dramatic performance implications.'
#         critical_string += '\n' + str(input_paths)
#         critical_string += '\n' + str(block_sizes)
#         L.critical(critical_string)
#
#     if n_workers is None:
#         print('num_cpu_available', str(multiprocessing.cpu_count()))
#         n_workers = 8
#         # n_workers = math.floor(multiprocessing.cpu_count() / 2) - 1 # For some reason, increasing this past like 8 even on a 128 core machine didn't help much. There must be some DASK magic utilizing all the cores even when n is low.
#     if memory_limit is None:
#         memory_limit = '8GB'
#     threads_per_worker = 2  # Cause hyperthreading
#     with LocalCluster(n_workers=n_workers, threads_per_worker=threads_per_worker, memory_limit=memory_limit) as cluster, Client(cluster) as client:
#         # with LocalCluster() as cluster, Client(cluster) as client:
#         # with LocalCluster(n_workers=math.floor(multiprocessing.cpu_count() / 2), threads_per_worker=2, memory_limit=str(math.floor(64 / (multiprocessing.cpu_count() + 1))) + 'GB') as cluster, Client(cluster) as client:
#
#         L.info('Starting Local Cluster at http://localhost:8787/status')
#
#         xds_list = []
#         for input_path in input_paths:
#             # xds = rioxarray.open_rasterio(input_path, chunks=(1, 512*4, 512*4), lock=False)
#             # xds = rioxarray.open_rasterio(input_path, chunks=(1, 512*4, 512*4), lock=False)
#             xds = rioxarray.open_rasterio(input_path, chunks='auto', lock=False)
#             xds_list.append(xds)
#
#         # Use reioxarray to read with specified chunksize.
#         zones_rxr = rioxarray.open_rasterio(zones_path, chunks={'band': 1, 'x': 1024, 'y': 1024})
#         values_rxr = rioxarray.open_rasterio(values_path, chunks={'band': 1, 'x': 1024, 'y': 1024})
#
#         # define the operation, which hasn't run yet.
#         subtraction = ds_scenario - ds_baseline
#
#         # Now it actually runs.
#         subtraction.compute()
#
#
#         delayed_computation = op(*xds_list)
#         delayed_computation.rio.to_raster(output_path, tiled=True, compress='DEFLATE', lock=Lock("rio", client=client))  # NOTE!!! MUCH FASTER WITH THIS. I think it's because it coordinates with the read to start the next thing asap.

def dask_sum_array(input_path):
    import dask
    from dask.distributed import Client, LocalCluster, Lock
    print('http://localhost:8787/status')
    with LocalCluster(n_workers=16, threads_per_worker=2, memory_limit='8GB') as cluster, Client(cluster) as client:
        hb.timer('Starting Local Cluster at http://localhost:8787/status')

        xds = rioxarray.open_rasterio(
            input_path,
            chunks={'band': 1, 'x': 1024, 'y': 1024},
            # chunks='auto',
            lock=False,
            # lock=Lock("rio", client=client)
            # lock=Lock("rio-read", client=client), # when too many file handles open
        )

        result = np.sum(xds)
        to_return = result.compute()
        return to_return

def zonal_statistics_dask(
    input_raster,
    zone_vector_path,
    zone_ids_raster_path=None,
    id_column_label=None,
    zones_raster_data_type=None,
    values_raster_data_type=None,
    zones_ndv=None,
    values_ndv=None,
    all_touched=None,
    assert_projections_same=True,
    unique_zone_ids=None,
    csv_output_path=None,
    vector_output_path=None,
    stats_to_retrieve='sums',
    enumeration_classes=None,
    multiply_raster_path=None,
    verbose=False,
    rewrite_zone_ids_raster=True,
    max_enumerate_value=1000,
):

    L.info('Launching dask_zonal_statistics.')

    # Test that input_raster and shapefile are in the same projection. Sillyness results if not.
    if assert_projections_same:
        hb.assert_gdal_paths_in_same_projection([input_raster, zone_vector_path])
    else:
        if verbose:
            a = hb.assert_gdal_paths_in_same_projection([input_raster, zone_vector_path], return_result=True)
            if not a:
                L.critical('Ran zonal_statistics_flex but the inputs werent in identical projections.')
        else:
            pass

    # if zone_ids_raster_path is not defined, use the PGP version, which doesn't use a rasterized approach.
    if not zone_ids_raster_path and rewrite_zone_ids_raster is False:
        to_return = pgp.zonal_statistics(
            base_raster_path_band, zone_vector_path,
            aggregate_layer_name=None, ignore_nodata=True,
            polygons_might_overlap=True, working_dir=None)
        if csv_output_path is not None:
            hb.python_object_to_csv(to_return, csv_output_path)
        return to_return

    # if zone_ids_raster_path is defined, then we are using a rasterized approach.
    # NOTE that by construction, this type of zonal statistics cannot handle overlapping polygons (each polygon is just represented by its id int value in the raster).
    else:
        if zones_ndv is None:
            zones_ndv = -9999

    if values_ndv is None:
        values_ndv = hb.get_raster_info_hb(input_raster)['nodata'][0]

    # Double check in case get_Raster fails
    if values_ndv is None:
        values_ndv = -9999.0

    # if zone_ids_raster_path is not set, make it a temporary file
    if zone_ids_raster_path is None:
        zone_ids_raster_path = 'zone_ids_' + hb.random_string() + '.tif'

    # if zone_ids_raster_path is given, use it to speed up processing (creating it first if it doesnt exist)
    if not hb.path_exists(zone_ids_raster_path) and rewrite_zone_ids_raster is not False:
        # Calculate the id raster and save it
        if verbose:
            L.info('Creating id_raster with convert_polygons_to_id_raster')
        hb.convert_polygons_to_id_raster(zone_vector_path, zone_ids_raster_path, input_raster, id_column_label=id_column_label, data_type=zones_raster_data_type,
                                         ndv=zones_ndv, all_touched=all_touched)
    else:
        if verbose:
            L.info('Zone_ids_raster_path existed, so not creating it.')

    # Much of the optimization happens by using sparse arrays rather than look-ups so that the index int is the id of the zone.
    if unique_zone_ids is None:
        gdf = gpd.read_file(zone_vector_path)
        if id_column_label is None:
            id_column_label = gdf.columns[0]

        unique_zone_ids_pre = np.unique(gdf[id_column_label][gdf[id_column_label].notnull()]).astype(np.int64)

        to_append = []
        if 0 not in unique_zone_ids_pre:
            to_append.append(0)
        # if zones_ndv not in unique_zone_ids_pre:
        #     to_append.append(zones_ndv)
        unique_zone_ids = np.asarray(to_append + list(unique_zone_ids_pre))
        # unique_zone_ids = np.asarray(to_append + list(unique_zone_ids_pre) + [max(unique_zone_ids_pre) + 1])

    if verbose:
        L.info('Starting zonal_statistics_rasterized using zone_ids_raster_path at ' + str(zone_ids_raster_path))

    # Call zonal_statistics_rasterized to parse vars into cython-format and go from there.

    if stats_to_retrieve == 'sums':
        L.debug('Exporting sums.')
        L.debug('unique_zone_ids', unique_zone_ids)
        r = hb.zonal_statistics_rasterized_dask(zone_ids_raster_path, input_raster, zones_ndv=zones_ndv, values_ndv=values_ndv, unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve, verbose=verbose)
        # unique_ids, sums = hb.zonal_statistics_rasterized(zone_ids_raster_path, input_raster, zones_ndv=zones_ndv, values_ndv=values_ndv,
        #                                                   unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve, verbose=verbose)
        print(r)
        unique_ids = None
        sums = None
        df = pd.DataFrame(index=unique_ids, data={'sums': sums})
        df[df == 0] = np.nan
        df.dropna(inplace=True)
        if csv_output_path is not None:
            df.to_csv(csv_output_path)

        if vector_output_path is not None:
            gdf = gpd.read_file(zone_vector_path)
            gdf = gdf.merge(df, how='outer', left_on=id_column_label, right_index=True)
            gdf.to_file(vector_output_path, driver='GPKG')

        return df

    elif stats_to_retrieve == 'sums_counts':
        L.debug('Exporting sums_counts.')
        unique_ids, sums, counts = hb.zonal_statistics_rasterized(zone_ids_raster_path, input_raster, zones_ndv=zones_ndv, values_ndv=values_ndv,
                                                                  unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve, verbose=verbose)

        df = pd.DataFrame(index=unique_ids, data={'sums': sums, 'counts': counts})
        df[df == 0] = np.nan
        df.dropna(inplace=True)
        if csv_output_path is not None:
            df.to_csv(csv_output_path)

        if vector_output_path is not None:
            gdf = gpd.read_file(zone_vector_path)
            gdf = gdf.merge(df, how='outer', left_on=id_column_label, right_index=True)
            gdf.to_file(vector_output_path, driver='GPKG')

        return df

    elif stats_to_retrieve == 'enumeration':
        L.debug('Exporting enumeration.')

        if enumeration_classes is None:
            enumeration_classes = hb.unique_raster_values_path(input_raster)

        unique_ids, enumeration = hb.zonal_statistics_rasterized(zone_ids_raster_path, input_raster, zones_ndv=zones_ndv, values_ndv=values_ndv,
                                                                 unique_zone_ids=unique_zone_ids, stats_to_retrieve=stats_to_retrieve,
                                                                 enumeration_classes=enumeration_classes, multiply_raster_path=multiply_raster_path,
                                                                 verbose=verbose, )
        enumeration = np.asarray(enumeration)
        df = pd.DataFrame(index=unique_ids, columns=[str(i) for i in list(range(0, len(enumeration_classes)))], data=enumeration)

        if vector_output_path is not None:
            gdf = gpd.read_file(zone_vector_path)
            gdf = gdf.merge(df, how='outer', left_on=id_column_label, right_index=True)
            gdf.to_file(vector_output_path, driver='GPKG')
            gdf_no_geom = gdf.drop(columns='geometry')

        if csv_output_path is not None:
            gdf_no_geom.to_csv(csv_output_path)

        return df

def unique_count_dask(input_path, n_workers=16, threads_per_worker=2, memory_limit='8GB'):
    import dask
    from dask.distributed import Client, LocalCluster, Lock

    with LocalCluster(n_workers=n_workers, threads_per_worker=threads_per_worker, memory_limit=memory_limit) as cluster, Client(cluster) as client:

        L.info('Starting Local Cluster at http://localhost:8787/status')

        dask_array = rioxarray.open_rasterio(input_path, chunks=(1, 512 * 4, 512 * 4), lock=False)
        dask_array_flat = dask.array.ravel(dask_array)

        unique_computation, counts_counts_computation = da.unique(dask_array_flat, return_counts=True)

        unique, counts = dask.compute(unique_computation, counts_counts_computation)
        result = dict(zip(unique, counts))

        return result
