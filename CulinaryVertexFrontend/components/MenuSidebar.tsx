import React, { useState } from 'react';
import { CloseIcon } from "@/components/CloseIcon";

// Define menu item type interface
interface MenuItem {
  category: string;
  menu_type: string[] | string;
  name: string;
  description?: string;
  price: number | { [key: string]: number };
  dietary?: string[];
  options?: string[];
  add_ons?: Array<{ item: string; price: number }>;
  sides?: string[];
  preparation?: string;
  enhancements?: Array<{ name: string; price: number; dietary?: string[] }>;
}

interface MenuSidebarProps {
  isOpen: boolean;
  toggleSidebar: () => void;
}

function MenuSidebar({ isOpen, toggleSidebar }: MenuSidebarProps) {
  // Add state for menu type filtering
  const [menuType, setMenuType] = useState<'All' | 'Lunch' | 'Dinner' | 'Drinks'>('All');
  
  // Parse menu data from paste.txt (already loaded in this example)
  const menuData: MenuItem[] = [
    {"category": "Raw/Chilled", "menu_type": ["Lunch", "Dinner"], "name": "Oysters on the Half Shell", "description": "chef's daily selection, hk mignonette, cocktail sauce", "price": {"half_dozen": 28.0, "full_dozen": 54.0}, "dietary": ["DF", "GF"]},
    {"category": "Raw/Chilled", "menu_type": ["Lunch", "Dinner"], "name": "Steak Tartare", "description": "sauce gribiche, crispy capers, cured egg yolk, brioche toast points", "price": 34.0},
    {"category": "Raw/Chilled", "menu_type": ["Lunch", "Dinner"], "name": "Shrimp Aguachile", "description": "cilantro vinaigrette, cucumber relish, espelette", "price": 26.0, "dietary": ["DF", "GF"]},
    {"category": "Raw/Chilled", "menu_type": ["Lunch", "Dinner"], "name": "Snapper Crudo", "description": "pickled mango purèe, fresno chile, tiger's milk, jalapeño oil, cilantro", "price": 26.0, "dietary": ["DF", "GF"]},
    {"category": "Raw/Chilled", "menu_type": ["Lunch", "Dinner"], "name": "Tuna Tartare", "description": "ahi tuna, soy chili vinaigrette, pickled fresno, asian pear, taro chips", "price": 28.0, "dietary": ["DF", "GF"]},
    {"category": "Appetizers", "menu_type": ["Lunch", "Dinner"], "name": "Harissa Flatbread", "description": "harissa butter, cilantro", "price": 12.0, "dietary": ["Vegetarian"]},
    {"category": "Appetizers", "menu_type": ["Lunch", "Dinner"], "name": "Truffled Oysters Rockefeller", "description": "truffle spinach ragout, fontina, herb crust", "price": 24.0},
    {"category": "Appetizers", "menu_type": "Lunch", "name": "Hellfire Hot Wings", "description": "hellfire sauce, blue cheese dressing", "price": 22.0},
    {"category": "Appetizers", "menu_type": ["Lunch", "Dinner"], "name": "Pan-Seared Scallops", "description": "celery root purée, braised bacon lardons, pickled granny smith apples, chives", "price": 32.0, "dietary": ["DF", "GF"], "options": ["vegan option available"]},
    {"category": "Appetizers", "menu_type": ["Lunch", "Dinner"], "name": "Lobster Risotto", "description": "butter-poached lobster tail, truffle, crispy onions", "price": 40.0, "options": ["vegan and vegetarian options available"]},
    {"category": "Appetizers", "menu_type": ["Lunch", "Dinner"], "name": "Wagyu Meatballs", "description": "american wagyu, pork, slow-roasted tomato sauce, polenta croutons, parmesan, basil", "price": 24.0},
    {"category": "Soup/Salads", "menu_type": ["Lunch", "Dinner"], "name": "Butternut Squash Soup", "description": "whipped goat cheese, roasted heirloom carrots, carrot chips", "price": 16.0, "dietary": ["GF", "Vegetarian"], "add_ons": [{"item": "grilled chicken", "price": 10.0}, {"item": "three chilled jumbo shrimp", "price": 14.0}]},
    {"category": "Soup/Salads", "menu_type": ["Lunch", "Dinner"], "name": "Harvest Salad", "description": "quinoa, kale, butternut squash, honeycrisp apple, cranberries, spiced pecans & pepitas, apple citrus vinaigrette", "price": 18.0, "dietary": ["GF", "Vegetarian"], "add_ons": [{"item": "grilled chicken", "price": 10.0}, {"item": "three chilled jumbo shrimp", "price": 14.0}]},
    {"category": "Soup/Salads", "menu_type": ["Lunch", "Dinner"], "name": "Caesar Salad", "description": "parmesan frico, garlic croutons, lemon zest", "price": {"full": 18.0, "side": 11.0}, "add_ons": [{"item": "grilled chicken", "price": 10.0}, {"item": "three chilled jumbo shrimp", "price": 14.0}]},
    {"category": "Sandwiches", "menu_type": "Lunch", "name": "Idiot Sandwich", "description": "pressed french bread, mojo spiced pork, sautéed peppers & onions, mustard sauce, swiss cheese, house pickles", "price": 26.0, "sides": ["french fries", "side market salad"]},
    {"category": "Sandwiches", "menu_type": "Lunch", "name": "Hell's Kitchen Burger", "description": "applewood-smoked bacon, ghost pepper cheese, fresno chili jam, mashed avocado, crispy onions, tomato, spicy aioli", "price": 27.0, "sides": ["french fries", "side market salad"]},
    {"category": "Sandwiches", "menu_type": "Lunch", "name": "Backyard Burger", "description": "american cheese, chopped pickles, red onion, OG sauce", "price": 25.0, "add_ons": [{"item": "applewood-smoked bacon", "price": 4.5}], "sides": ["french fries", "side market salad"]},
    {"category": "Sandwiches", "menu_type": "Lunch", "name": "Steak Sandwich", "description": "toasted ciabatta, filet, grilled onions, gruyère, arugula, whole grain mustard, lemon aioli", "price": 28.0, "sides": ["french fries", "side market salad"]},
    {"category": "Sandwiches", "menu_type": "Lunch", "name": "Crab Roll", "description": "mashed avocado, aji amarillo, pickled fresno", "price": 28.0, "sides": ["french fries", "side market salad"]},
    {"category": "Mains", "menu_type": "Lunch", "name": "Petite Beef Wellington", "description": "potato purée, glazed root vegetables, red wine demi-glace", "price": 44.0, "preparation": "served medium rare"},
    {"category": "Mains", "menu_type": "Lunch", "name": "Roasted Chicken", "description": "parsnip purée, roasted root vegetables, crispy sage, apple chicken jus", "price": 42.0, "dietary": ["GF"]},
    {"category": "Mains", "menu_type": "Lunch", "name": "Crispy Skin Salmon", "description": "coconut green curry, sticky rice, thai apple slaw", "price": 44.0, "dietary": ["DF", "GF"]},
    {"category": "Mains", "menu_type": "Lunch", "name": "8 oz.... Filet Mignon", "description": "herb-roasted tomato, charred scallion, horseradish hollandaise", "price": 68.0, "dietary": ["GF"]},
    {"category": "Mains", "menu_type": "Lunch", "name": "Tofu Fried Rice", "description": "cabbage, kale, spiced cashews, sesame seeds, peanut sauce", "price": 26.0, "dietary": ["DF", "GF", "Vegan"]},
    {"category": "Pizzas", "menu_type": "Lunch", "name": "Margherita", "description": "slow-roasted tomato sauce, fresh mozzarella, roasted tomatoes", "price": 20.0, "dietary": ["Vegetarian"]},
    {"category": "Pizzas", "menu_type": "Lunch", "name": "Mushroom", "description": "truffle gouda cheese sauce, mushrooms, grilled onions, spinach", "price": 21.0, "dietary": ["Vegetarian"]},
    {"category": "Pizzas", "menu_type": "Lunch", "name": "Hell's Kitchen", "description": "slow-roasted tomato sauce, sriracha, pepperoni, bacon, avocado crema, jalapeño honey", "price": 22.0},
    {"category": "Sides", "menu_type": "Lunch", "name": "French Fries", "description": "fancy sauce", "price": 12.0, "dietary": ["Vegetarian"]},
    {"category": "Sides", "menu_type": ["Lunch", "Dinner"], "name": "Elotes", "description": "roasted corn, crema, hot sauce, cotija, cilantro, lime", "price": 14.0, "dietary": ["GF", "Vegetarian"]},
    {"category": "Sides", "menu_type": ["Lunch", "Dinner"], "name": "Potato Purée", "description": "crème fraîche, chives", "price": 14.0, "dietary": ["GF", "Vegetarian"]},
    {"category": "Sides", "menu_type": "Dinner", "name": "Baked Macaroni & Cheese", "description": "smoked gouda sauce, crispy prosciutto, chives", "price": 17.0},
    {"category": "Sides", "menu_type": "Dinner", "name": "Potato Gratin", "description": "garlic cream sauce, parmesan, fontina, chives", "price": 15.0, "dietary": ["GF"]},
    {"category": "Sides", "menu_type": "Dinner", "name": "Roasted Brussels Sprouts", "description": "chili glaze, pickled fresno peppers, cilantro", "price": 16.0, "dietary": ["DF"]},
    {"category": "Entrées", "menu_type": "Dinner", "name": "Beef Wellington", "description": "potato purée, glazed root vegetables, red wine demi-glace", "price": 74.0, "preparation": "served medium rare", "enhancements": [{"name": "lobster tail", "price": 32.0, "dietary": ["GF"]}, {"name": "garlic butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "foie gras", "price": 20.0, "dietary": ["DF", "GF"]}, {"name": "truffle butter", "price": 6.0, "dietary": ["GF", "V"]}, {"name": "crab oscar", "price": 28.0, "dietary": ["GF"]}, {"name": "herb butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "seasonal truffles", "price": 29.0, "dietary": ["DF", "GF"]}]},
    {"category": "Entrées", "menu_type": "Dinner", "name": "Roasted Chicken", "description": "parsnip purée, roasted root vegetables, crispy sage, apple chicken jus", "price": 36.0, "dietary": ["GF"], "enhancements": [{"name": "lobster tail", "price": 32.0, "dietary": ["GF"]}, {"name": "garlic butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "foie gras", "price": 20.0, "dietary": ["DF", "GF"]}, {"name": "truffle butter", "price": 6.0, "dietary": ["GF", "V"]}, {"name": "crab oscar", "price": 28.0, "dietary": ["GF"]}, {"name": "herb butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "seasonal truffles", "price": 29.0, "dietary": ["DF", "GF"]}]},
    {"category": "Entrées", "menu_type": "Dinner", "name": "Crispy Skin Salmon", "description": "coconut green curry, sticky rice, thai apple slaw", "price": 44.0, "dietary": ["DF", "GF"], "enhancements": [{"name": "lobster tail", "price": 32.0, "dietary": ["GF"]}, {"name": "garlic butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "foie gras", "price": 20.0, "dietary": ["DF", "GF"]}, {"name": "truffle butter", "price": 6.0, "dietary": ["GF", "V"]}, {"name": "crab oscar", "price": 28.0, "dietary": ["GF"]}, {"name": "herb butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "seasonal truffles", "price": 29.0, "dietary": ["DF", "GF"]}]},
    {"category": "Entrées", "menu_type": "Dinner", "name": "Grilled Branzino", "description": "sauce vierge, swiss chard, almond gremolata, roasted cherry tomatoes", "price": 60.0, "dietary": ["DF", "GF"], "enhancements": [{"name": "lobster tail", "price": 32.0, "dietary": ["GF"]}, {"name": "garlic butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "foie gras", "price": 20.0, "dietary": ["DF", "GF"]}, {"name": "truffle butter", "price": 6.0, "dietary": ["GF", "V"]}, {"name": "crab oscar", "price": 28.0, "dietary": ["GF"]}, {"name": "herb butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "seasonal truffles", "price": 29.0, "dietary": ["DF", "GF"]}]},
    {"category": "Entrées", "menu_type": "Dinner", "name": "Braised Short Rib", "description": "yukon potato cake, spinach, crispy onions, red wine demi-glace", "price": 48.0, "dietary": ["DF"], "enhancements": [{"name": "lobster tail", "price": 32.0, "dietary": ["GF"]}, {"name": "garlic butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "foie gras", "price": 20.0, "dietary": ["DF", "GF"]}, {"name": "truffle butter", "price": 6.0, "dietary": ["GF", "V"]}, {"name": "crab oscar", "price": 28.0, "dietary": ["GF"]}, {"name": "herb butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "seasonal truffles", "price": 29.0, "dietary": ["DF", "GF"]}]},
    {"category": "Entrées", "menu_type": "Dinner", "name": "8 Oz.... Filet Mignon", "description": "herb-roasted tomato, charred scallion, horseradish hollandaise", "price": 68.0, "dietary": ["GF"], "enhancements": [{"name": "lobster tail", "price": 32.0, "dietary": ["GF"]}, {"name": "garlic butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "foie gras", "price": 20.0, "dietary": ["DF", "GF"]}, {"name": "truffle butter", "price": 6.0, "dietary": ["GF", "V"]}, {"name": "crab oscar", "price": 28.0, "dietary": ["GF"]}, {"name": "herb butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "seasonal truffles", "price": 29.0, "dietary": ["DF", "GF"]}]},
    {"category": "Entrées", "menu_type": "Dinner", "name": "20 Oz.... Prime Bone-In Ribeye", "description": "roasted garlic, glazed maitake mushrooms, peppercorn sauce", "price": 95.0, "dietary": ["GF"], "enhancements": [{"name": "lobster tail", "price": 32.0, "dietary": ["GF"]}, {"name": "garlic butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "foie gras", "price": 20.0, "dietary": ["DF", "GF"]}, {"name": "truffle butter", "price": 6.0, "dietary": ["GF", "V"]}, {"name": "crab oscar", "price": 28.0, "dietary": ["GF"]}, {"name": "herb butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "seasonal truffles", "price": 29.0, "dietary": ["DF", "GF"]}]},
    {"category": "Entrées", "menu_type": "Dinner", "name": "Tofu Fried Rice", "description": "cabbage, kale, spiced cashews, sesame seeds, peanut sauce", "price": 26.0, "dietary": ["DF", "GF", "Vegan"], "enhancements": [{"name": "lobster tail", "price": 32.0, "dietary": ["GF"]}, {"name": "garlic butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "foie gras", "price": 20.0, "dietary": ["DF", "GF"]}, {"name": "truffle butter", "price": 6.0, "dietary": ["GF", "V"]}, {"name": "crab oscar", "price": 28.0, "dietary": ["GF"]}, {"name": "herb butter", "price": 4.0, "dietary": ["GF", "V"]}, {"name": "seasonal truffles", "price": 29.0, "dietary": ["DF", "GF"]}]},
    {"category": "Appetizers", "menu_type": "Dinner", "name": "Grilled Octopus", "description": "white bean purée, pee wee potatoes, roasted tomatoes, chili oil, chimichurri", "price": 32.0, "dietary": ["GF"]},
    {"category": "Dessert", "menu_type": ["Lunch", "Dinner"], "name": "Sticky Toffee Pudding", "description": "english toffee sauce, ice cream", "price": 18.0, "dietary": ["Vegetarian"]},
    {"category": "Dessert", "menu_type": ["Lunch", "Dinner"], "name": "Chocolate Orange Trifle", "description": "citrus-soaked chocolate sponge, orange gelée, chocolate mousse, chantilly cream, candied hazelnuts", "price": 17.0, "dietary": ["Vegetarian"]},
    {"category": "Dessert", "menu_type": ["Lunch", "Dinner"], "name": "Lemon Blueberry Cheesecake", "description": "graham cracker crust, lemon curd, blueberry compote", "price": 15.0, "dietary": ["Vegetarian"]},
    {"category": "Dessert", "menu_type": ["Lunch", "Dinner"], "name": "Pineapple Carpaccio", "description": "coconut sorbet, passion fruit, coconut flakes, lime", "price": 16.0, "dietary": ["DF", "GF", "Vegan"]},
    {"category": "Coffee", "menu_type": "Drinks", "name": "Drip Coffee by La Colombe", "price": 4.0},
    {"category": "Coffee", "menu_type": "Drinks", "name": "Espresso Coffee by La Colombe", "price": 4.0},
    {"category": "Coffee", "menu_type": "Drinks", "name": "Cappuccino & Latte Coffee by La Colombe", "price": 5.0},
    {"category": "Digestif", "menu_type": "Drinks", "name": "Nonino Quintessencia Amaro", "price": 15.0},
    {"category": "Digestif", "menu_type": "Drinks", "name": "Montenegro Amaro", "price": 14.0},
    {"category": "Digestif", "menu_type": "Drinks", "name": "Fernet Branca Amaro", "price": 14.0},
    {"category": "Digestif", "menu_type": "Drinks", "name": "Cynar Amaro", "price": 16.0},
    {"category": "Cognac", "menu_type": "Drinks", "name": "Remy Martin, Louis XIII", "description": "2 oz", "price": 500.0},
    {"category": "Cognac", "menu_type": "Drinks", "name": "Hennessy XO", "price": 85.0},
    {"category": "Cognac", "menu_type": "Drinks", "name": "Hennessy Paradis", "price": 300.0},
    {"category": "Grappa", "menu_type": "Drinks", "name": "Jacopo Poli, Moscato", "price": 35.0},
    {"category": "Grappa", "menu_type": "Drinks", "name": "Jacopo Poli, Torcolato", "price": 35.0},
    {"category": "Grappa", "menu_type": "Drinks", "name": "Jacopo Poli, Vespaiolo", "price": 35.0},
    {"category": "Fortified Wine", "menu_type": "Drinks", "name": "Dow's 10 Year Tawny", "price": 18.0},
    {"category": "Fortified Wine", "menu_type": "Drinks", "name": "Gould Campbell Vintage 1997", "price": 35.0},
    {"category": "Sweet Wine", "menu_type": "Drinks", "name": "Royal Tokaji 5 Puttonyos Tokaji Aszu", "price": 21.0},
    {"category": "Sweet Wine", "menu_type": "Drinks", "name": "Anselmi Recioto 'I Capitelli'", "price": 23.0},
    {"category": "Sparkling", "menu_type": "Drinks", "name": "Montelvini Prosecco", "description": "asolo docg, italy nv", "price": 15.0},
    {"category": "Sparkling", "menu_type": "Drinks", "name": "Albrecht Crémant d'Alsace", "description": "brut rosé, alsace, france nv", "price": 15.0},
    {"category": "Sparkling", "menu_type": "Drinks", "name": "Louis Massing Blanc de Blanc", "description": "grand cru champagne, france nv", "price": 33.0},
    {"category": "White/Rosé", "menu_type": "Drinks", "name": "Sauvignon Blanc, Lauvertat", "description": "\"moulin des vrillères\" sancerre, loire valley, france 2023", "price": 20.0},
    {"category": "White/Rosé", "menu_type": "Drinks", "name": "Sauvignon Blanc, Flannery Hill", "description": "marlborough, new zealand 2021", "price": 15.0},
    {"category": "White/Rosé", "menu_type": "Drinks", "name": "Pinot Grigio, Scarpetta", "description": "friuli, italy 2022", "price": 13.0},
    {"category": "White/Rosé", "menu_type": "Drinks", "name": "Riesling, Gunderloch", "description": "\"jean-baptiste\" kabinett, rheinhessen, germany 2022", "price": 15.0},
    {"category": "White/Rosé", "menu_type": "Drinks", "name": "Chardonnay, Domaine Brigitte Cerveau", "description": "chablis, burgundy, france 2022", "price": 23.0},
    {"category": "White/Rosé", "menu_type": "Drinks", "name": "Chardonnay, Timbre Winery", "description": "santa maria valley, california 2018", "price": 20.0},
    {"category": "White/Rosé", "menu_type": "Drinks", "name": "Viognier, Michael Shaps Wineworks", "description": "charlottesville, va 2023", "price": 19.0},
    {"category": "White/Rosé", "menu_type": "Drinks", "name": "Grenache, Peyrassol", "description": "\"la croix des templiers\", méditerranée igp, france 2023", "price": 14.0},
    {"category": "Red Wine", "menu_type": "Drinks", "name": "Pinot Noir, La Follette", "description": "\"los primeros\", sonoma, california 2021", "price": 18.0},
    {"category": "Red Wine", "menu_type": "Drinks", "name": "Pinot Noir, G&B Rion", "description": "\"la croix blanche\", burgundy, france 2021", "price": 24.0},
    {"category": "Red Wine", "menu_type": "Drinks", "name": "Sangiovese, Rodano", "description": "chianti classico tuscany, italy 2020", "price": 15.0},
    {"category": "Red Wine", "menu_type": "Drinks", "name": "Saperavi, KGM Kindzmarauli", "description": "semi-sweet, republic of georgia 2022", "price": 16.0},
    {"category": "Red Wine", "menu_type": "Drinks", "name": "Tempranillo, C.V.N.E.", "description": "\"cune\", reserve, rioja, spain 2018", "price": 19.0},
    {"category": "Red Wine", "menu_type": "Drinks", "name": "Merlot, Trig Point", "description": "alexander valley, california 2022", "price": 17.0},
    {"category": "Red Wine", "menu_type": "Drinks", "name": "Malbec, Cuveliar Los Andes", "description": "mendoza, argentina 2019", "price": 17.0},
    {"category": "Red Wine", "menu_type": "Drinks", "name": "Cabernet Sauvignon, L'Esprit de Chevalier", "description": "pessac-leognac, bordeaux, france 2018", "price": 28.0},
    {"category": "Red Wine", "menu_type": "Drinks", "name": "Cabernet Sauvignon, Daou", "description": "paso robles, california 2022", "price": 18.0},
    {"category": "Cocktails", "menu_type": "Drinks", "name": "Fujiwhara Effect", "description": "blackstrap rum, lime, fresh pineapple, house made ginger beer", "price": 19.0},
    {"category": "Cocktails", "menu_type": "Drinks", "name": "Poire You Always Hating", "description": "tequila blanco, lime, ménage au poire, fino, candied walnut", "price": 20.0},
    {"category": "Cocktails", "menu_type": "Drinks", "name": "A Diving Bell", "description": "london dry gin, yuzu, mezcal, pineapple gomme, cayenne", "price": 21.0},
    {"category": "Lager", "menu_type": "Drinks", "name": "Bud Light", "description": "st. louis, mo", "price": 7.0},
    {"category": "Lager", "menu_type": "Drinks", "name": "Stella Artois", "description": "belgium", "price": 9.0},
    {"category": "Lager", "menu_type": "Drinks", "name": "Estrella Jalisco", "description": "mexico", "price": 8.0},
    {"category": "Lager", "menu_type": "Drinks", "name": "Ayinger \"Celebrator\"", "description": "germany", "price": 10.0},
    {"category": "Cider", "menu_type": "Drinks", "name": "Bold Rock \"IPA\"", "description": "charlottesville, va", "price": 8.0},
    {"category": "Ale", "menu_type": "Drinks", "name": "Port City \"Optimal Wit\"", "description": "witbier, alexandria, va", "price": 7.0},
    {"category": "Ale", "menu_type": "Drinks", "name": "Westmalle", "description": "trappist tripel, belgium", "price": 14.0},
    {"category": "Ale", "menu_type": "Drinks", "name": "Bear Republic \"Racer 5\"", "description": "ipa, cloverdale, ca", "price": 8.0},
    {"category": "Ale", "menu_type": "Drinks", "name": "Solace \"Little Bit Cloudy\"", "description": "new england ipa, chantilly, va", "price": 8.0},
    {"category": "Mocktails", "menu_type": "Drinks", "name": "Lychee Cooler", "description": "lychee, grapefruit, elderflower, lime juice", "price": 11.0},
    {"category": "Mocktails", "menu_type": "Drinks", "name": "Hibiscus Sour", "description": "hibiscus tea, lemon, simple syrup", "price": 10.0},
    {"category": "Cocktails", "menu_type": "Drinks", "name": "Obligatory Vodka Drink", "description": "vodka, fresh grapefruit, peychauds, pamplemousse cordial, pink peppercorn", "price": 18.0},
    {"category": "Cocktails", "menu_type": "Drinks", "name": "Red Eye Old Fashioned", "description": "bourbon, demerara gomme, hints of tobacco leaf & roasted coffee", "price": 22.0},
    {"category": "Cocktails", "menu_type": "Drinks", "name": "Espresso Martini", "description": "tequila reposado, espresso, kahlúa, vanilla", "price": 23.0},
    {"category": "Cocktails", "menu_type": "Drinks", "name": "Eighteen Stars", "description": "tequila reposado, cointreau, yellow pepper, passion fruit, lime", "price": 21.0},
    {"category": "Cocktails", "menu_type": "Drinks", "name": "Smoke On The Water", "description": "rye, aperol, averna amaro, sweet vermouth, smoked with cherry wood", "price": 24.0},
    {"category": "Cocktails", "menu_type": "Drinks", "name": "Notes From Gordon", "description": "dry gin, green tea, lemongrass, peach, lemon, message from gordon", "price": 19.0}
  ];
  
  
  // Filter menu items based on selected type
  const filteredMenu = menuData.filter(item => {
    if (menuType === 'All') return true;
    if (menuType === 'Drinks') return item.menu_type === 'Drinks';
    
    if (Array.isArray(item.menu_type)) {
      return item.menu_type.includes(menuType);
    }
    return item.menu_type === menuType;
  });
  
  // Group menu items by category
  const groupedMenu: { [key: string]: MenuItem[] } = {};
  filteredMenu.forEach(item => {
    if (!groupedMenu[item.category]) {
      groupedMenu[item.category] = [];
    }
    groupedMenu[item.category].push(item);
  });
  
  // Format price display for different price structures
  const formatPrice = (price: number | { [key: string]: number }): string => {
    if (typeof price === 'number') {
      return `$${price}`;
    } else {
      const prices = Object.values(price);
      if (prices.length === 1) {
        return `$${prices[0]}`;
      } else {
        const min = Math.min(...prices);
        const max = Math.max(...prices);
        return `$${min}-${max}`;
      }
    }
  };
  
  // Define category order for display
  const foodCategories = [
    'Raw/Chilled',
    'Appetizers',
    'Soup/Salads',
    'Sandwiches',
    'Mains',
    'Pizzas',
    'Entrées',
    'Sides',
    'Dessert'
  ];
  
  const drinkCategories = [
    'Cocktails',
    'Mocktails',
    'Red Wine',
    'White/Rosé',
    'Sparkling',
    'Lager',
    'Ale',
    'Cider',
    'Coffee'
  ];
  
  // Choose appropriate category order based on filter
  const categoryOrder = menuType === 'Drinks' ? drinkCategories : foodCategories;
  
  // Get sorted categories that exist in our filtered menu
  const sortedCategories = categoryOrder.filter(cat => groupedMenu[cat]);
  
  return (
    <div className={`menu-sidebar fixed left-0 top-16 h-[calc(100%-64px)] bg-[var(--lk-bg)] border-r border-white/10 w-80 transition-transform duration-300 z-40 ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
      <div className="p-4 border-b border-white/10 flex justify-between items-center">
        <h3 className="text-white font-semibold">Our Menu</h3>
        <button onClick={toggleSidebar} className="text-white/70 hover:text-white">
          <CloseIcon />
        </button>
      </div>
      
      {/* Filter buttons */}
      <div className="p-4 border-b border-white/10 flex flex-wrap gap-2">
        <button 
          onClick={() => setMenuType('All')}
          className={`px-3 py-1 rounded text-sm ${menuType === 'All' ? 'bg-amber-600 text-white' : 'bg-white/10 text-white/70 hover:bg-white/20'}`}
        >
          All
        </button>
        <button 
          onClick={() => setMenuType('Lunch')}
          className={`px-3 py-1 rounded text-sm ${menuType === 'Lunch' ? 'bg-amber-600 text-white' : 'bg-white/10 text-white/70 hover:bg-white/20'}`}
        >
          Lunch
        </button>
        <button 
          onClick={() => setMenuType('Dinner')}
          className={`px-3 py-1 rounded text-sm ${menuType === 'Dinner' ? 'bg-amber-600 text-white' : 'bg-white/10 text-white/70 hover:bg-white/20'}`}
        >
          Dinner
        </button>
        <button 
          onClick={() => setMenuType('Drinks')}
          className={`px-3 py-1 rounded text-sm ${menuType === 'Drinks' ? 'bg-amber-600 text-white' : 'bg-white/10 text-white/70 hover:bg-white/20'}`}
        >
          Drinks
        </button>
      </div>
      
      {/* Menu items by category */}
      <div className="p-4 h-[calc(100%-128px)] overflow-y-auto">
        {sortedCategories.length > 0 ? (
          sortedCategories.map(category => (
            <div key={category} className="mb-6">
              <h4 className="text-amber-500 font-semibold mb-3 text-lg">{category}</h4>
              <div className="space-y-4">
                {groupedMenu[category].map((item, index) => (
                  <div key={index} className="border-b border-white/10 pb-3">
                    <div className="flex justify-between">
                      <h5 className="text-white font-medium">{item.name}</h5>
                      <span className="text-white">{formatPrice(item.price)}</span>
                    </div>
                    {item.description && (
                      <p className="text-white/70 text-sm mt-1">{item.description}</p>
                    )}
                    {item.dietary && (
                      <p className="text-amber-400 text-xs mt-1">
                        {item.dietary.join(", ")}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          ))
        ) : (
          <p className="text-white/70 text-center mt-8">No menu items available for this selection.</p>
        )}
      </div>
      
      <button onClick={toggleSidebar} className="absolute bottom-4 left-4 px-4 py-2 rounded bg-amber-600 text-white text-sm hover:bg-amber-500">
        Close Menu
      </button>
    </div>
  );
}

export default MenuSidebar;
