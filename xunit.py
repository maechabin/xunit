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
    def run(self):
        # TestResultのインスタンスを生成
        result = TestResult()
        result.testStarted()
        self.setUp()
        try:
            method = getattr(self, self.name)
            method()
        # 例外をキャッチ
        except:
            result.testFailed()
        self.tearDown()
        return result

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
    # テストメソッドが実行されたかテスト
    def testTemplateMethod(self):
        # WasRunのインスタンスを生成（Fixture）
        test = WasRun('testMethod')
        test.run()
        assert('setUp testMethod tearDown ' == test.log)
    # テスト結果を返すかテスト（成功時）
    def testResult(self):
        # WasRunのインスタンスを生成（Fixture）
        test = WasRun('testMethod')
        result = test.run()
        assert('1 run, 0 failed' == result.summary())
    # テスト結果を返すかテスト（失敗時）
    def testFailedResult(self):
        # WasRunのインスタンスを生成（Fixture）
        test = WasRun('testBrokenMethod')
        result = test.run()
        assert('1 run, 1 failed' == result.summary())
    # テストが失敗しても期待した内容がきちんと出力されるか
    def testFailedResultFormatting(self):
        # TestResultのインスタンスを作成
        result = TestResult()
        result.testStarted()
        result.testFailed()
        assert('1 run, 1 failed' == result.summary())

print(TestCaseTest('testTemplateMethod').run().summary())
print(TestCaseTest('testResult').run().summary())
print(TestCaseTest('testFailedResult').run().summary())
print(TestCaseTest('testFailedResultFormatting').run().summary())
