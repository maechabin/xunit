class TestResult:
    def __init__(self):
        # 実行した数を0で初期化
        self.runCount = 0
        # 失敗の数を0で初期化
        self.errorCount = 0
    def testStarted(self):
        # テスト実行ごとにインクリメント
        self.runCount = self.runCount + 1
    def testFailed(self):
        # テスト失敗ごとにインクリメント
        self.errorCount = self.errorCount + 1
    def summary(self):
        return '%d run, %d failed' % (self.runCount, self.errorCount);

class TestCase:
    def __init__(self, name):
        self.name = name
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def run(self, result):
        result.testStarted()
        self.setUp()
        try:
            method = getattr(self, self.name)
            method()
        # 例外をキャッチ
        except:
            result.testFailed()
        self.tearDown()

class TestSuite:
    def __init__(self):
        # テストリスト
        self.tests = []
    def add(self, test):
        # テストをリストへ追加
        self.tests.append(test)
    def run(self, result):
        for test in self.tests:
            test.run(result)

class WasRun(TestCase):
    def setUp(self):
        # 呼び出されたメソッドを記録するログを保持する
        self.log = 'setUp '
    def testMethod(self):
        # テストメソッドの実行をログに記録する
        self.log = self.log + 'testMethod '
    def testBrokenMethod(self):
        # 例外を投げる
        raise Exception
    def tearDown(self):
        # tearDownメソッドの実行をログに記録する
        self.log = self.log + 'tearDown '

class TestCaseTest(TestCase):
    def setUp(self):
        self.result = TestResult()
    # テストメソッドが実行されたかテスト
    def testTemplateMethod(self):
        # WasRunのインスタンスを生成（Fixture）
        test = WasRun('testMethod')
        test.run(self.result)
        assert('setUp testMethod tearDown ' == test.log)
    # テスト結果を返すかテスト（成功時）
    def testResult(self):
        # WasRunのインスタンスを生成（Fixture）
        test = WasRun('testMethod')
        test.run(self.result)
        assert('1 run, 0 failed' == self.result.summary())
    # テスト結果を返すかテスト（失敗時）
    def testFailedResult(self):
        # WasRunのインスタンスを生成（Fixture）
        test = WasRun('testBrokenMethod')
        test.run(self.result)
        assert('1 run, 1 failed' == self.result.summary())
    # テストが失敗しても期待した内容がきちんと出力されるか
    def testFailedResultFormatting(self):
        # TestResultのインスタンスを作成
        self.result.testStarted()
        self.result.testFailed()
        assert('1 run, 1 failed' == self.result.summary())
    # いくつかのテストを登録し、収集された実行結果を取得するテスト
    def testSuite(self):
        suite = TestSuite()
        suite.add(WasRun('testMethod'))
        suite.add(WasRun('testBrokenMethod'))
        suite.run(self.result)
        assert('2 run, 1 failed' == self.result.summary())

suite = TestSuite()
suite.add(TestCaseTest('testTemplateMethod'))
suite.add(TestCaseTest('testResult'))
suite.add(TestCaseTest('testFailedResult'))
suite.add(TestCaseTest('testFailedResultFormatting'))
suite.add(TestCaseTest('testSuite'))
result = TestResult()
suite.run(result)
print(result.summary())