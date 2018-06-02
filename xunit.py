class TestCase:
    def __init__(self, name):
        self.name = name
    def setUp(self):
        pass
    def run(self):
        self.setUp()
        method = getattr(self, self.name)
        method()

class WasRun(TestCase):
    def setUp(self):
        # 呼び出されたメソッドを記録するログを保持する
        self.log = 'setUp '
    def testMethod(self):
        # テストメソッドの実行をログに記録する
        self.log = self.log + 'testMethod '

class TestCaseTest(TestCase):
    # テストメソッド    
    def testTemplateMethod(self):
        # WasRunのインスタンスを生成（Fixture）
        test = WasRun('testMethod')
        test.run()
        assert('setUp testMethod ' == test.log)

TestCaseTest('testTemplateMethod').run()