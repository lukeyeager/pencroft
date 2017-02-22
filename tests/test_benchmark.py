from pencroft.benchmark import benchmark


class TestBenchmark:
    def test_benchmark(self, mytest_path):
        benchmark(mytest_path)

    def test_benchmark_4thread(self, mytest_path):
        benchmark(mytest_path, threads=4)

    def test_benchmark_4proc(self, mytest_path):
        benchmark(mytest_path, threads=4,
                  thread_library='multiprocessing')
