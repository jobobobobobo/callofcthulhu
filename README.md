# callofcthulhu
Python scripts for working with Chaosium's Call of Cthulhu.

I like to play Call of Cthulhu as a Keeper. I want to have programmatic tools for managing the rules of the game.

Current features:
1. A HumanCharacter class that represents a character in the rules.
  a. HumanCharacter has methods that interact with various skills and calculate derived stats. 
2. A Skill contains a checkbox (necessary for improvement), a name, and a score. It also keeps track of what rules set it is from and whether it should be considered important.
  a. I plan to use the 'important' field to denote occupation skills and other things that actually get points. That way a player can query their character for ideas to roll.
  b. The Skill class also has plumbing to level it up, add points without a roll, and of course make a roll.
  c. So a HumanCharacter will make a skill_roll, which actually calls the skill itself.
3. A Dice library that I'm proud of. It handles exploding dice (I also run World of Darkness) and fudge dice (why not). 
  a. The thing I like is that the result is determined when you call the constructor. You can store a result for later, keep a history of rolls, and other things like that by extending the Die class.
  
  Planned features:
  1. Walking you through character creation
  2. Commiting investigators to JSON or some other format for MongoDB or something like that.
  3. Support for rules sets like Byakhee does. I have run 6th edition and Laundry Files, and I am running 7th edition going forward. So I want to support them all.
  4. Support for non-human characters. Ideally I want to be able to define a character type and be able to generate them on the fly. Instead of rolling ghouls ahead of time I can make them on the fly.
  5. A gui??? someday?????
