import csv
import json
import os
import time
import pytest
from boonamber import AmberClient, AmberUserError, AmberCloudError, float_list_to_csv_string
from amber_secrets import get_secrets

amber = None
sensor_id = None

# secrets downloaded from points beyond
def create_amber_client():
    amber_license_file = os.environ.get('AMBER_TEST_LICENSE_FILE', None)
    amber_license_id = os.environ.get('AMBER_TEST_LICENSE_ID', None)
    assert amber_license_id is not None, 'AMBER_TEST_LICENSE_ID is missing in test environment'

    # purge AMBER environment variables
    for key in Test_01_AmberInstance.saved_env.keys():
        if key in os.environ:
            del os.environ[key]

    if amber_license_file is not None:
        # load license profile using a local license file
        amber_client = AmberClient(amber_license_id, amber_license_file)
    else:
        # load license profile from secrets manager
        secret_dict = get_secrets()
        license_profile = secret_dict.get(amber_license_id, None)
        os.environ['AMBER_USERNAME'] = license_profile['username']
        os.environ['AMBER_PASSWORD'] = license_profile['password']
        os.environ['AMBER_SERVER'] = license_profile['server']
        os.environ['AMBER_OAUTH_SERVER'] = license_profile['oauth-server']
        amber_client = AmberClient(None, None)

    return amber_client


class Test_01_AmberInstance:
    # class variable to saved license file name from environment
    saved_env = {
        'AMBER_LICENSE_FILE': None,
        'AMBER_USERNAME': None,
        'AMBER_PASSWORD': None,
        'AMBER_SERVER': None,
        'AMBER_OAUTH_SERVER': None,
        'AMBER_LICENSE_ID': None,
        'AMBER_SSL_CERT': None
    }

    @staticmethod
    def clear_environment():
        for key in Test_01_AmberInstance.saved_env:
            if key in os.environ:
                Test_01_AmberInstance.saved_env[key] = os.environ.get(key, None)
                del os.environ[key]

    @staticmethod
    def restore_environment():
        for key, value in Test_01_AmberInstance.saved_env.items():
            if value is not None:
                os.environ[key] = value
            elif key in os.environ:
                del os.environ[key]

    def test_01_init(self):

        Test_01_AmberInstance.clear_environment()

        # load profile using license file specified as parameter
        profile1 = AmberClient(license_file='test.Amber.license')

        # load the same profile using license loaded from environment
        os.environ['AMBER_LICENSE_FILE'] = 'test.Amber.license'
        profile2 = AmberClient()
        assert profile1.license_profile == profile2.license_profile, 'override with AMBER_LICENSE_FILE'

        # override items in license file through environment
        os.environ['AMBER_USERNAME'] = "xyyyAmberUser"
        os.environ['AMBER_PASSWORD'] = "bogus_password"
        os.environ['AMBER_SERVER'] = "https://temp.amber.boonlogic.com/v1"
        os.environ['AMBER_SSL_CERT'] = "bogus_ssl_cert"
        os.environ['AMBER_SSL_VERIFY'] = "false"
        profile3 = AmberClient(license_file='test.Amber.license')
        assert profile3.license_profile['server'] == "https://temp.amber.boonlogic.com/v1"
        assert profile3.license_profile['username'] == "xyyyAmberUser"
        assert profile3.license_profile['password'] == "bogus_password"
        assert profile3.license_profile['cert'] == "bogus_ssl_cert"
        assert profile3.license_profile['verify'] == False

        # set configuration through environment with non-existent license file
        os.environ['AMBER_USERNAME'] = "EnvironmentAmberUser"
        os.environ['AMBER_PASSWORD'] = "bogus_password"
        os.environ['AMBER_SERVER'] = "https://temp.amber.boonlogic.com/v1"
        os.environ['AMBER_SSL_CERT'] = "bogus_ssl_cert"
        os.environ['AMBER_SSL_VERIFY'] = "false"
        profile4 = AmberClient(license_file='bogus.Amber.license')
        assert profile4.license_profile['server'] == "https://temp.amber.boonlogic.com/v1"
        assert profile4.license_profile['username'] == "EnvironmentAmberUser"
        assert profile4.license_profile['password'] == "bogus_password"
        assert profile4.license_profile['cert'] == "bogus_ssl_cert"
        assert profile4.license_profile['verify'] == False

        Test_01_AmberInstance.restore_environment()

    def test_02_init_negative(self):

        Test_01_AmberInstance.clear_environment()

        # no license file specified
        with pytest.raises(AmberUserError):
            AmberClient(license_id="default", license_file="nonexistent-license-file")

        # missing required fields
        os.environ['AMBER_LICENSE_FILE'] = "test.Amber.license"
        with pytest.raises(AmberUserError):
            AmberClient(license_id="nonexistent-license-id", license_file="test.Amber.license")
        with pytest.raises(AmberUserError):
            AmberClient(license_id="missing-username", license_file="test.Amber.license")
        with pytest.raises(AmberUserError):
            AmberClient(license_id="missing-password", license_file="test.Amber.license")
        with pytest.raises(AmberUserError):
            AmberClient(license_id="missing-server", license_file="test.Amber.license")

        Test_01_AmberInstance.restore_environment()


class Test_02_Authenticate:

    def test_01_authenticate(self):
        amber = create_amber_client()
        print(json.dumps(amber.license_profile, indent=4))
        amber._authenticate()
        assert amber.token is not None
        assert amber.token != ''

    def test_02_authenticate_negative(self):
        amber = create_amber_client()
        # modify the password
        amber.license_profile['password'] = "not-valid"
        with pytest.raises(AmberCloudError) as context:
            amber._authenticate()
        assert context.value.code == 401


class Test_03_SensorOps:

    def test_00_init(self):
        global amber, sensor_id
        amber = create_amber_client()
        sensor_id = amber.create_sensor('test-sensor-python')

    def test_01_create_sensor(self):
        global amber, sensor_id
        try:
            assert sensor_id is not None
            assert sensor_id != ""
        except Exception as e:
            raise RuntimeError("setup failed: {}".format(e))

    def test_02_update_label(self):
        global amber, sensor_id
        label = amber.update_label(sensor_id, 'new-label')
        assert label == 'new-label'

        try:
            amber.update_label(sensor_id, 'test-sensor-python')
        except Exception as e:
            raise RuntimeError("teardown failed, label was not changed back to 'test-sensor-python': {}".format(e))

    def test_03_update_label_negative(self):
        global amber, sensor_id
        with pytest.raises(AmberCloudError) as context:
            label = amber.update_label('nonexistent-sensor-id', 'test-sensor-python')
        assert context.value.code == 404

    def test_04_get_sensor(self):
        global amber, sensor_id
        sensor = amber.get_sensor(sensor_id)
        assert sensor['label'] == 'test-sensor-python'
        assert sensor['sensorId'] == sensor_id
        assert 'usageInfo' in sensor

    def test_05_get_sensor_negative(self):
        global amber, sensor_id
        with pytest.raises(AmberCloudError) as context:
            sensor = amber.get_sensor('nonexistent-sensor-id')
        assert context.value.code == 404

    def test_06_list_sensors(self):
        global amber, sensor_id
        sensors = amber.list_sensors()
        assert sensor_id in sensors.keys()

    def test_07_configure_sensor(self):
        global amber, sensor_id
        # configure sensor with custom features
        expected = {
            'featureCount': 1,
            'streamingWindowSize': 25,
            'samplesToBuffer': 1000,
            'anomalyHistoryWindow': 1000,
            'learningRateNumerator': 10,
            'learningRateDenominator': 10000,
            'learningMaxClusters': 1000,
            'learningMaxSamples': 1000000,
            'features': [{
                'minVal': 1,
                'maxVal': 50,
                'label': 'fancy-label',
                'submitRule': 'submit'
            }]
        }
        features = [{
            'minVal': 1,
            'maxVal': 50,
            'label': 'fancy-label'
        }]
        config = amber.configure_sensor(sensor_id, feature_count=1,
                                                          streaming_window_size=25,
                                                          samples_to_buffer=1000,
                                                          anomaly_history_window=1000,
                                                          learning_rate_numerator=10,
                                                          learning_rate_denominator=10000,
                                                          learning_max_clusters=1000,
                                                          learning_max_samples=1000000,
                                                          features=features)

        assert config == expected

        # configure sensor with default features
        expected = {
            'featureCount': 1,
            'streamingWindowSize': 25,
            'samplesToBuffer': 1000,
            'anomalyHistoryWindow': 1000,
            'learningRateNumerator': 10,
            'learningRateDenominator': 10000,
            'learningMaxClusters': 1000,
            'learningMaxSamples': 1000000,
            'features': [{
                'maxVal': 1,
                'minVal': 0,
                'label': 'feature-0',
                'submitRule': 'submit'
            }]
        }
        config = amber.configure_sensor(sensor_id, feature_count=1,
                                                          streaming_window_size=25,
                                                          samples_to_buffer=1000,
                                                          anomaly_history_window=1000,
                                                          learning_rate_numerator=10,
                                                          learning_rate_denominator=10000,
                                                          learning_max_clusters=1000,
                                                          learning_max_samples=1000000)
        assert config == expected

        # configure sensor with percent variation overridden
        config = amber.configure_sensor(sensor_id, feature_count=1,
                                                          streaming_window_size=25,
                                                          samples_to_buffer=1000,
                                                          anomaly_history_window=1000,
                                                          learning_rate_numerator=10,
                                                          learning_rate_denominator=10000,
                                                          learning_max_clusters=1000,
                                                          learning_max_samples=1000000,
                                                          override_pv=.055)
        expected['percentVariationOverride'] = .055
        assert config == expected

    def test_07_configure_sensor_negative(self):
        global amber, sensor_id
        with pytest.raises(AmberCloudError) as context:
            config = amber.configure_sensor('nonexistent-sensor-id')
        assert context.value.code == 404

        # invalid feature_count or streaming_window_size
        pytest.raises(AmberUserError, amber.configure_sensor, sensor_id, feature_count=-1)
        with pytest.raises(AmberUserError):
            amber.configure_sensor(sensor_id, feature_count=1.5)
        with pytest.raises(AmberUserError):
            amber.configure_sensor(sensor_id, streaming_window_size=-1)
        with pytest.raises(AmberUserError):
            amber.configure_sensor(sensor_id, streaming_window_size=1.5)

    def test_08_get_config(self):
        global amber, sensor_id
        expected = {
            'featureCount': 1,
            'streamingWindowSize': 25,
            'samplesToBuffer': 1000,
            'anomalyHistoryWindow': 1000,
            'learningRateNumerator': 10,
            'learningRateDenominator': 10000,
            'learningMaxClusters': 1000,
            'learningMaxSamples': 1000000,
            'percentVariation': 0.055,
            'percentVariationOverride': 0.055,
            'features': [{'minVal': 0, 'maxVal': 1, 'label': 'feature-0', 'submitRule': 'submit'}]
        }
        config = amber.get_config(sensor_id)
        assert config == expected

    def test_09_get_config_negative(self):
        global amber, sensor_id
        with pytest.raises(AmberCloudError) as context:
            config = amber.get_config('nonexistent-sensor-id')
        assert context.value.code == 404

    def test_10_configure_fusion(self):
        global amber, sensor_id
        # fusion tests setup
        amber.configure_sensor(sensor_id, feature_count=5, streaming_window_size=1)

        f = [{'label': 'f{}'.format(i), 'submitRule': 'submit'} for i in range(5)]
        resp = amber.configure_fusion(sensor_id, features=f)
        assert resp == f

    def test_11_configure_fusion_negative(self):
        global amber, sensor_id
        f = [{'label': 'f{}'.format(i), 'submitRule': 'submit'} for i in range(5)]

        # missing sensor
        with pytest.raises(AmberCloudError) as context:
            amber.configure_fusion('nonexistent-sensor-id', features=f)
        assert context.value.code == 404

        # number of features doesn't match configured feature_count
        with pytest.raises(AmberCloudError) as context:
            amber.configure_fusion(sensor_id, features=f[:4])
        assert context.value.code == 400

        # duplicate feature in configuration
        badf = f.copy()
        badf[3] = badf[2]
        with pytest.raises(AmberCloudError) as context:
            amber.configure_fusion(sensor_id, features=badf)
        assert context.value.code == 400

        # unrecognized submit rule in configuration
        badf = f.copy()
        badf[2]['submitRule'] = 'badsubmitrule'
        with pytest.raises(AmberCloudError) as context:
            amber.configure_fusion(sensor_id, features=badf)
        assert context.value.code == 400

    def test_12_stream_fusion(self):
        global amber, sensor_id

        # stream partial vector (204 response)
        v = [{'label': 'f1', 'value': 2}, {'label': 'f3', 'value': 4}]
        exp = {'vector': "None,2,None,4,None"}
        resp = amber.stream_fusion(sensor_id, vector=v)
        assert resp == exp

        # stream full vector (200 response)
        v = [{'label': 'f0', 'value': 1}, {'label': 'f2', 'value': 3}, {'label': 'f4', 'value': 5}]
        exp = {
            'vector': "1,2,3,4,5",
            'results': {
                'clusterCount': 0,
                'message': '',
                'progress': 0,
                'retryCount': 0,
                'state': "Buffering",
                'streamingWindowSize': 1,
                'totalInferences': 0,
                'lastModified': 123456789,
                'lastModifiedDelta': 1,
                'AD': [0], 'AH': [0], 'AM': [0], 'AW': [0], 'ID': [0], 'RI': [0], 'SI': [0],
                'NI': [0], 'NS': [0], 'NW': [0], 'OM': [0]
            }
        }
        resp = amber.stream_fusion(sensor_id, vector=v)
        assert resp.keys() == exp.keys()

    def test_13_stream_fusion_negative(self):
        global amber, sensor_id
        # fusion vector contains label not in fusion configuration
        v = [{'label': 'badfeature', 'value': 2}, {'label': 'f3', 'value': 4}]
        with pytest.raises(AmberCloudError) as context:
            amber.stream_fusion(sensor_id, vector=v)
        assert context.value.code == 400

        # fusion vector contains duplicate label
        v = [{'label': 'f3', 'value': 2}, {'label': 'f3', 'value': 4}]
        with pytest.raises(AmberCloudError) as context:
            amber.stream_fusion(sensor_id, vector=v)
        assert context.value.code == 400

        # fusion tests teardown
        amber.configure_sensor(sensor_id, feature_count=1,
                                                 streaming_window_size=25)  # teardown

    def test_14_stream_sensor(self):
        global amber, sensor_id
        results = amber.stream_sensor(sensor_id, 1)
        assert 'state' in results
        assert 'message' in results
        assert 'progress' in results
        assert 'clusterCount' in results
        assert 'retryCount' in results
        assert 'streamingWindowSize' in results
        assert 'lastModified' in results
        assert 'lastModifiedDelta' in results
        assert 'SI' in results
        assert 'AD' in results
        assert 'AH' in results
        assert 'AM' in results
        assert 'AW' in results
        assert 'NI' in results
        assert 'NS' in results
        assert 'NW' in results
        assert 'OM' in results

        # scalar data should return SI of length 1
        assert len(results['SI']) == 1

        # array data should return SI of same length
        results = amber.stream_sensor(sensor_id, [1, 2, 3, 4, 5])
        assert len(results['SI']) == 5

    def test_15_stream_sensor_negative(self):
        global amber, sensor_id
        with pytest.raises(AmberCloudError) as context:
            results = amber.stream_sensor('nonexistent-sensor-id', [1, 2, 3, 4, 5])
        assert context.value.code == 404

        # invalid data
        with pytest.raises(AmberUserError):
            amber.stream_sensor(sensor_id, [])
        with pytest.raises(AmberUserError):
            amber.stream_sensor(sensor_id, [1, '2', 3])
        with pytest.raises(AmberUserError):
            amber.stream_sensor(sensor_id, [1, [2, 3], 4])

    def test_16_post_outage(self):
        global amber, sensor_id
        results = amber.post_outage(sensor_id)
        assert "Buffering" == results["state"]

        results = amber.stream_sensor(sensor_id, [1, 2, 3, 4, 5])
        assert list(set(results['ID'])) == [0]

    def test_17_post_outage_negative(self):
        global amber, sensor_id
        with pytest.raises(AmberCloudError) as context:
            results = amber.post_outage('nonexistent-sensor-id')
        assert context.value.code == 404

    def test_18_get_root_cause(self):
        global amber, sensor_id
        config = amber.get_config(sensor_id)
        expected = [[0] * len(config['features']) * config['streamingWindowSize']] * 2
        config = amber.get_root_cause(sensor_id,
                                                        pattern_list=[
                                                            [1] * len(config['features']) * config[
                                                                'streamingWindowSize'],
                                                            [0] * len(config['features']) * config[
                                                                'streamingWindowSize']])
        assert config == expected

    def test_19_get_root_cause_negative(self):
        global amber, sensor_id
        with pytest.raises(AmberCloudError) as context:
            config = amber.get_root_cause('nonexistent-sensor-id', id_list=[1])
        assert context.value.code == 404

        # give both fail
        with pytest.raises(AmberUserError) as context:
            config = amber.get_root_cause(sensor_id, id_list=[1],
                                                            pattern_list=[[1, 2, 3], [4, 5, 6]])

        # give neither fail
        with pytest.raises(AmberUserError) as context:
            config = amber.get_root_cause(sensor_id)

        with pytest.raises(AmberCloudError):
            amber.get_root_cause(sensor_id, [1])

    def test_20_get_status(self):
        global amber, sensor_id
        status = amber.get_status(sensor_id)
        assert 'pca' in status
        assert 'numClusters' in status

    def test_21_get_status_negative(self):
        global amber, sensor_id
        with pytest.raises(AmberCloudError) as context:
            status = amber.get_status('nonexistent-sensor-id')
        assert context.value.code == 404

    def test_22_get_pretrain_state(self):
        global amber, sensor_id
        response = amber.get_pretrain_state(sensor_id)
        assert 'state' in response
        assert response['state'] == 'None'

    def test_23_get_pretrain_state_negative(self):
        with pytest.raises(AmberCloudError) as context:
            response = amber.get_pretrain_state('nonexistent-sensor-id')
        assert context.value.code == 404

    def test_24_pretrain_sensor(self):
        global amber, sensor_id
        with open('output_current.csv', 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            data = []
            for row in csv_reader:
                for d in row:
                    data.append(float(d))

        results = amber.pretrain_sensor(sensor_id, data, block=True)
        assert results['state'] == 'Pretrained'

        results = amber.pretrain_sensor(sensor_id, data, block=False)
        assert 'Pretraining' in results['state'] or 'Pretrained' in results['state']
        while True:
            time.sleep(5)
            results = amber.get_pretrain_state(sensor_id)
            if results['state'] == 'Pretraining':
                continue
            else:
                break
        assert results['state'] == 'Pretrained'

    def test_24a_pretrain_xl_sensor(self):
        global amber, sensor_id
        with open('output_current.csv', 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            data = []
            for row in csv_reader:
                for d in row:
                    data.append(float(d))

        results = amber.pretrain_sensor_xl(sensor_id, data, block=True,
                                                             chunk_size=100000)
        assert results['state'] == 'Pretrained'

        results = amber.pretrain_sensor_xl(sensor_id, data, block=False,
                                                             chunk_size=100000)
        assert 'Pretraining' in results['state'] or 'Pretrained' in results['state']
        while True:
            time.sleep(5)
            results = amber.get_pretrain_state(sensor_id)
            if results['state'] == 'Pretraining':
                continue
            else:
                break
        assert results['state'] == 'Pretrained'

    def test_25_pretrain_sensor_negative(self):
        global amber, sensor_id
        with pytest.raises(AmberCloudError) as context:
            response = amber.pretrain_sensor('123456abcdef', [1, 2, 3, 4, 5], block=True)
        assert context.value.code == 404

        # not enough data to fill sample buffer
        with pytest.raises(AmberCloudError) as context:
            response = amber.pretrain_sensor(sensor_id, [1, 2, 3, 4, 5], block=True)
        assert context.value.code == 400

    def test_25a_pretrain_sensor_negative(self):
        global amber, sensor_id
        with pytest.raises(AmberCloudError) as context:
            response = amber.pretrain_sensor_xl('123456abcdef', [1, 2, 3, 4, 5], block=True)
        assert context.value.code == 404

        # send a chunk size that is too big
        with pytest.raises(AmberCloudError) as context:
            response = amber.pretrain_sensor_xl(sensor_id, [1, 2, 3, 4, 5],
                                                                  block=True, chunk_size=4000001)
        assert context.value.code == 400

    def test_26_enable_learning(self):
        global amber, sensor_id
        # enable learning tests setup
        exp = {
            "learningRateNumerator": 10,
            "learningRateDenominator": 10000,
            "learningMaxClusters": 1000,
            "learningMaxSamples": 1000000
        }
        resp = amber.enable_learning(sensor_id,
                                                       learning_rate_numerator=10,
                                                       learning_rate_denominator=10000,
                                                       learning_max_clusters=1000,
                                                       learning_max_samples=1000000)
        assert resp == exp

    def test_27_enable_learning_negative(self):
        global amber, sensor_id
        exp = {"streaming": {
            "learningRateNumerator": 10,
            "learningRateDenominator": 10000,
            "learningMaxClusters": 1000,
            "learningMaxSamples": 1000000}
        }
        # missing sensor
        with pytest.raises(AmberCloudError) as context:
            amber.enable_learning('nonexistent-sensor-id', learning_max_samples=1000000)
        assert context.value.code == 404

        with pytest.raises(AmberCloudError) as context:
            amber.enable_learning(sensor_id, learning_max_samples=-1)
        assert context.value.code == 400

        # not in learning state
        amber.configure_sensor(sensor_id, feature_count=5, streaming_window_size=1)
        with pytest.raises(AmberCloudError) as context:
            amber.enable_learning(sensor_id, learning_max_samples=1000000)
        assert context.value.code == 400

    def test_28_delete_sensor_negative(self):
        global amber, sensor_id
        with pytest.raises(AmberCloudError) as context:
            amber.delete_sensor('nonexistent-sensor-id')
        assert context.value.code == 404

    def test_29_delete_sensor(self):
        global amber, sensor_id
        try:
            amber.delete_sensor(sensor_id)
        except Exception as e:
            raise RuntimeError("teardown failed, sensor was not deleted: {}".format(e))


class Test_04_ApiReauth:

    def test_api_reauth(self):
        # create amber instance and mark auth_time
        amber = create_amber_client()
        saved_reauth_time = amber.reauth_time

        # first call covers reauth case, reauth time should be set bigger than initial time
        _ = amber.list_sensors()
        assert amber.reauth_time > saved_reauth_time
        saved_reauth_time = amber.reauth_time

        _ = amber.list_sensors()
        # The reauth time should not have changed
        assert amber.reauth_time == saved_reauth_time

        # Add 60 to the reauth_time and reissue api call, reauth should occur
        amber.reauth_time += 61
        _ = amber.list_sensors()
        assert amber.reauth_time > saved_reauth_time


class Test_04_CSVConvert:

    def test_convert_to_csv(self):
        amber = create_amber_client()

        # valid scalar inputs
        assert "1.0" == float_list_to_csv_string(1)
        assert "1.0" == float_list_to_csv_string(1.0)

        # valid 1d inputs
        assert "1.0,2.0,3.0" == float_list_to_csv_string([1, 2, 3])
        assert "1.0,2.0,3.0" == float_list_to_csv_string([1, 2, 3.0])
        assert "1.0,2.0,3.0" == float_list_to_csv_string([1.0, 2.0, 3.0])

        # valid 2d inputs
        assert "1.0,2.0,3.0,4.0" == float_list_to_csv_string([[1, 2], [3, 4]])
        assert "1.0,2.0,3.0,4.0" == float_list_to_csv_string([[1, 2, 3, 4]])
        assert "1.0,2.0,3.0,4.0" == float_list_to_csv_string([[1], [2], [3], [4]])
        assert "1.0,2.0,3.0,4.0" == float_list_to_csv_string([[1, 2], [3, 4.0]])
        assert "1.0,2.0,3.0,4.0" == float_list_to_csv_string([[1.0, 2.0], [3.0, 4.0]])

    def test_convert_to_csv_negative(self):
        amber = create_amber_client()

        # empty data
        with pytest.raises(ValueError): float_list_to_csv_string([])
        with pytest.raises(ValueError): float_list_to_csv_string([[]])
        with pytest.raises(ValueError): float_list_to_csv_string([[], []])

        # non-numeric data
        with pytest.raises(ValueError):
            float_list_to_csv_string(None)
        with pytest.raises(ValueError):
            float_list_to_csv_string('a')
        with pytest.raises(ValueError):
            float_list_to_csv_string('abc')
        with pytest.raises(ValueError):
            float_list_to_csv_string([1, None, 3])
        with pytest.raises(ValueError):
            float_list_to_csv_string([1, 'a', 3])
        with pytest.raises(ValueError):
            float_list_to_csv_string([1, 'abc', 3])
        with pytest.raises(ValueError):
            float_list_to_csv_string([[1, None], [3, 4]])
        with pytest.raises(ValueError):
            float_list_to_csv_string([[1, 'a'], [3, 4]])
        with pytest.raises(ValueError):
            float_list_to_csv_string([[1, 'abc'], [3, 4]])

        # badly-shaped data
        with pytest.raises(ValueError):
            float_list_to_csv_string([1, [2, 3], 4])  # mixed nesting
        with pytest.raises(ValueError):
            float_list_to_csv_string([[1, 2], [3, 4, 5]])  # ragged array
        with pytest.raises(ValueError):
            float_list_to_csv_string([[[1, 2, 3, 4]]])  # nested too deep
        with pytest.raises(ValueError):
            float_list_to_csv_string([[[1], [2], [3], [4]]])


class Test_05_Version:

    def test_01_version(self):
        amber = create_amber_client()
        version = amber.get_version()
        assert 'builder' in version.keys()
        assert 'expert-api' in version.keys()
        assert 'expert-common' in version.keys()
        assert 'nano-secure' in version.keys()
        assert 'api-version' in version.keys()
        assert 'release' in version.keys()
