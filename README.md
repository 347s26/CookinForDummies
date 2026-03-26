# CookinForDummies

## People
Rea Lotlikar, Nia Ameen, Will Upright, Jordan Phelps

## Purpose
To help college students reduce waste and save money by helping them find recipes to make with ingredients and utensils they have within their household. It also will help beginner chefs by providing information on basic cooking skills. It will also be a place to store recipes all together making it easier to locate them when needed. Overall the main purpose of our application will be to improve college students' meals and cooking abilities.

## Users
Targeted towards college students (years of dining halls creates people who struggle with cooking) 
Also targets low income people so they can save money from using what they already have within the home

Application will assist these groups of people because it provides a free simple way to best utilize resources that you already have within home, allowing users to save money while also trying new tasty meals. (Also should help users in removing the urge to order takeout because they think it sounds good when they’re able to see tasty recipes they could create at home)

## Features
Entering ingredients that the user had
	Entering equipment that the user has
	Generate recipes from the given ingredients
	Store recipes that have been used in the past
	Offer substitutions if a recipe contains something the user doesn't have?
	Tell users possible ingredients they can buy to pair with what they have to create this other recipe
	Tell users possible equipment they could buy to create new recipes from ingredients they already have
	Rate recipes you tried App suggests similar recipes that you’d like based on ratings	Filters out recipes based on allergies 
	A learning feature where users are able to “level up” after they complete certain skills such as dicing an onion then next level would be caramelizing an onion
	It tracks ingredients that you have before and after using a certain recipe

## Data
CRUD: Users will create new recipes by uploading / updating the ingredients and equipment they have available. Users will also be able to delete recipes or remove ingredients / equipment. Users will also define possible allergies to limit/restrict recipes.

Nav bar: 
Home  My Recipes  Skills  About  Search  Profile 

Models: 

    Ingredient (
		Name: text
		Unit: text choice
		Amount: double
	)
	
	Utensils(
		Name: text
	)

	Appliance(
		Name: text
	)

	Recipe(
		Title: text
		Ingredients: Foreign Key(Ingredient)
		Utensils: Foreign Key(Utensil)
		Steps: text
		TimeToMake: integer
		Rating: int
		Required Skills: Foreign Key(Skill)
	)

	Allergies(
		Ingredient: Foreign Key (Ingredient)
	)
	
	Skill(
		Name: text
		Video: url
	)
