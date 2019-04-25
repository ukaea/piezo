import system_load_tests

if __name__ == '__main__':
    piezo_base_url = 'http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo'
    system_load_results = system_load_tests.run_system_load_tests(piezo_base_url, [1, 3, 10])
