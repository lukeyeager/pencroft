from pencroft.benchmark import benchmark


class TestLoader:
    """Generic loader tests, should pass for all loaders"""

    def test_keys(self, mytest_loader, mytest_keys):
        assert sorted(mytest_keys) == sorted(mytest_loader.keys())

    def test_benchmark(self, mytest_path):
        benchmark(mytest_path)

    def test_benchmark_4thread(self, mytest_path):
        benchmark(mytest_path, threads=4)

    def test_benchmark_4proc(self, mytest_path):
        benchmark(mytest_path, threads=4,
                  thread_library='multiprocessing')
