import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from testing import create_backbone, TestModelBase


# class TestModelBaseCase(TestModelBase):

#     class TestModel(

#     def test_put_to_db(self):




class TestBackboneModel(TestModelBase):

    def test_template(self):
        backbone = create_backbone()
        self.put_to_db(backbone)
        objs = self.get_all('Backbone')



if __name__ == '__main__':
    unittest.main()

