#pylint: disable=C0103,C0111,W0611
"Unit tests para el calculo lambda"
import unittest

from Clambda import process_entry

class TestLambdaParser(unittest.TestCase):

    def test_zero(self):
        self.assertEqual(
            process_entry("0"),
            "0:Nat"
        )

    def test_true(self):
        self.assertEqual(
            process_entry("true"),
            "True:Bool"
        )

    def test_branches_with_diff_types(self):
        with self.assertRaises(TypeError):
            process_entry("if true then 0 else false")

    def test_lambda_wo_var(self):
        self.assertEqual(
            process_entry("\\x:Nat.succ(0)"),
            "\\x:Nat.succ(0):Nat->Nat"
        )

    def test_lambda_w_var(self):
        self.assertEqual(
            process_entry("\\z:Nat.z"),
            "\\z:Nat.z:Nat->Nat"
        )

    def test_succ_with_bool(self):
        with self.assertRaises(TypeError):
            process_entry("(\\x:Bool.succ(x)) true")

    def test_succ(self):
        self.assertEqual(
            process_entry("succ(succ(succ(0)))"),
            "succ(succ(succ(0))):Nat"
        )

    def test_free_variable(self):
        with self.assertRaises(KeyError):
            process_entry("x")

    def test_succ_pred(self):
        self.assertEqual(
            process_entry("succ(succ(pred(0)))"),
            "succ(0):Nat"
        )

    def test_lambda(self):
        self.assertEqual(
            process_entry("\\x:Nat.succ(x)"),
            "\\x:Nat.succ(x):Nat->Nat"
        )

    def test_wrong_app(self):
        with self.assertRaises(TypeError):
            process_entry("0 0")

    def test_complex_lambda(self):
        self.assertEqual(
            process_entry("\\x:Nat->Nat.\\y:Nat.(\\z:Bool.if z then x y else 0)"),
            "\\x:Nat->Nat.\\y:Nat.(\\z:Bool.if z then x y else 0):(Nat->Nat)->(Nat->(Bool->Nat))"
        )

    def test_complex_lambda_eval(self):
        self.assertEqual(
            process_entry("(\\x:Nat->Nat.\\y:Nat.(\\z:Bool.if z then x y else 0)) (\\j:Nat.succ(j)) succ(succ(succ(succ(succ(succ(succ(succ(0)))))))) true"),
            "succ(succ(succ(succ(succ(succ(succ(succ(succ(0))))))))):Nat"
        )

if __name__ == "__main__":
    unittest.main()
