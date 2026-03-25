from . import TeviTestBase
from ..items import all_item_table
class TestLocationCheck(TeviTestBase):
    def test_Linebomb(self) -> None:
        location = ["North Thanatara Canyon - Blueberry Bunny Potion"]
        items = [["Cross Bomb"],["Cluster Bomb"]]
        self.assertAccessDependency(location,items,only_check_listed=True)

    def test_LibraryAcess(self) -> None:
        location = "Ana Thema - Sable"
        items = [self.get_item_by_name("Cross Bomb"),self.get_item_by_name("Library Key")]
        self.collect(items)
        self.assertTrue(self.can_reach_location(location))

    def test_Hands(self) -> None:
        location = "Forest Maze extended - Gilded Exultation"
        items = [self.get_item_by_name("Gilded Left Hand"),self.get_item_by_name("Gilded Right Hand"),self.get_item_by_name("Cross Bomb"),self.get_item_by_name("Double Rabi Boots")]
        self.collect(items)
        self.assertTrue(self.can_reach_location(location))

    def test_locations(self) -> None:
        items = self.collect_all_but([""])
        self.assertTrue(self.can_reach_location("Ulskan Village Area - Grape Bunny Potion"))
        self.assertTrue(self.can_reach_location("Cloister Main - C. Rank Frenzy: Focus MAX"))


class TestItems(TeviTestBase):
    run_default_tests = None
    options = {
        "randomize_money": "1",
        "randomize_magitite": "1",
        "randomize_mananite": "1",
        "start_inventory":{
            "Running Boots": 3,
            "Trinketeer's Fortune": 3,
            "Bag Expander": 5
            }
    }
    def test_ProgressionItemCount(self):
        itemList = {}
        for item in self.multiworld.get_items():
            if item in itemList:
                itemList[item] +=1
            else:
                itemList[item] = 1
        for k,v in itemList.items():
            if k.trap or "EVENT" in k.name:
                continue
            if not k.advancement and all_item_table[k.name].category == "Consumeable":
                continue
            default_quantity = all_item_table[k.name].default_quantity
            self.assertFalse(v>default_quantity,f"{k}: {v}>{default_quantity}")


class TestMemine(TeviTestBase):
    run_default_tests = None
    options = {
        "open_morose": "1",
    }
    
    def test_Memine_Ticket(self) -> None:
        items =[self.get_item_by_name("Tartarus VIP Pass"),self.get_item_by_name("Valhalla VIP Pass")]
        
        locations = "Valhalla City - Memine Race From Tartarus"
        self.collect(items)
        self.assertFalse(self.can_reach_location(locations))
        self.assertTrue(self.can_reach_region("Tartarus"))

    def test_Forest_to_Copperwood(self) -> None:
        locations = ["CopperWood - Memine Race from Forest"]
        items = []
        self.collect(items)
        self.assertFalse(self.can_reach_location("CopperWood - Memine Race from Forest"))


class TestGalleryOfSouls(TeviTestBase):
    run_default_tests = None
    options = {
        "traverse_Mode": "random_teleporter",
    }
    
    def test_gallery_of_souls(self) -> None:
        items =[self.get_item_by_name("Cluster Bomb"),self.get_item_by_name("Slick Boots"),self.get_item_by_name("Double Rabi Boots"),self.get_item_by_name("Teleporter Gallery of Souls")]
        
        locations = "Gallery of Souls - Double Rabi Boots"
        self.collect(items)
        self.assertFalse(self.can_reach_location(locations))

