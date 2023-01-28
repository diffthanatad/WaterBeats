from edge_data_processor import edge_data_processor


webserver = edge_data_processor("localhost", 5500, True)
webserver.runserver()