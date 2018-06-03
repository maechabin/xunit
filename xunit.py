class TestResult:
    def __init__(self):
        self.runCount = 0
    def testStarted(self):
        self.runCount = self.runCount + 1
    def summary(self):
        return '%d run, 0 failed' % self.runCount;

class TestCase:
    def __init__(self, name):
        self.name = name
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def run(self):
        result = TestResult()
        result.testStarted()
        self.setUp()
        method = getattr(self, self.name)
        method()
        self.tearDown()
        return result

class WasRun(TestCase):
    def setUp(self):
        # 呼び出されたメソッドを記録するログを保持する
        self.log = 'setUp '
    def testMethod(self):
        # テストメソッドの実行をログに記録する
        self.log = self.log + 'testMethod '
    def tearDown(self):
        # tearDownメソッドの実行をログに記録する
        self.log = self.log + 'tearDown '

class TestCaseTest(TestCase):
    # テストメソッドが実行されたかテスト
    def testTemplateMethod(self):
        # WasRunのインスタンスを生成（Fixture）
        test = WasRun('testMethod')
        test.run()
        assert('setUp testMethod tearDown ' == test.log)
    # テスト結果を返すかテスト
    def testResult(self):
        # WasRunのインスタンスを生成（Fixture）
        test = WasRun('testMethod')
        result = test.run()
        assert('1 run, 0 failed' == result.summary())

TestCaseTest('testTemplateMethod').run()
TestCaseTest('testResult').run()
