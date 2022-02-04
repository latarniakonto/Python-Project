# Expression game


<p>
    <img src="https://i.imgur.com/NPrfg9n.png" width="400" height="300" />
    <img src="https://i.imgur.com/GMvmSKf.png" width="400" height="300" />
</p>

## Requirements
To run this game you have to install the following pip3 packages:
*sqlalchemy* and *pygame*

## How to run it?
This game should be run from withing the main folder. It is because path to *Font* and *Sprites* folder is hard coded in *expression_game.py*

Run these commands int this order to play the game: <br/>
`python3 App/expression_creator.py` <br/>
`python3 App/expression_game.py`

If you want to also run tests:
<body>
    <details>
        <summary>    
        </summary>
        I modified the path using context, hence the tests should be run from within Test folder (abspath "../App/" is set up) <br/>
        python3 test_suite.py
    </details>
</body>

## Flow diagram
![](https://i.imgur.com/KMcEK7T.png)
