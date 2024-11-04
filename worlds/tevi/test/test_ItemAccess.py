from . import TeviTestBase

class TestLocationCheck(TeviTestBase):
    def test_Test(self) -> None:
        locations = ["Thanatara Canyon - Cross Bomb"]
        items= []
        self.assertTrue(locations,items)

    def test_Linebomb(self) -> None:
        location = ["North Thanatara Canyon - Blueberry Bunny Potion"]
        items = [["Cross Bomb"]]
        self.assertAccessDependency(location,items,only_check_listed=True)

    def test_LibraryAcess(self) -> None:
        location = ["Ana Thema - Sable"]
        items = ["Cross Bomb","Library Key"]
        self.assertTrue(location,items)

    def test_Hands(self) -> None:
        location = ["Forest Maze extended - Gilded Exultation"]
        items = ["Gilded Left Hand","Gilded Right Hand","Cross Bomb","Double Rabi Boots"]
        self.assertTrue(location,items)

    def test_locations(self) -> None:
        items = self.collect_all_but([""])
        self.assertTrue(["Ulskan Village Area - Grape Bunny Potion"])



