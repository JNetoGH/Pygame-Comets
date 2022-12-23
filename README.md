# COMETS
link: https://github.com/JNetoGH/Farm-Game

<br>

## ALUNOS
João Neto (a22200558):
- desenvolvimento da game  engine
- arquitetura do game
- desenvolvimento do controle de fluxo do game
- desenvolvimento geral dos GameObjects

Margarida Teles (a22204247):
- desenvolvimento das artes para UI e Sprites
- assistência no desenvolvimento de mecânicas
- assistência no desenvolvimento de prefabs
- assistência nas layers
- assistência na criação do mapa

<br>

## GAME-ENGINE (quick overview)

### ENGINE VS JOGO EM MINHA ARQUITETURA
O jogo está separado em pastas, há pastas exclusivas da JNeto Productions Game Engine, esta é uma ferramenta discreta, o jogo em si é composto por GameObjects, os quais não ficam localizados juntamente da engine, porém, acessam seus recursos, tais quais, Systems, GameLoop, Components, Scenes, Prefabs, RenderingLayers e Cameras.

Com isso em mente, eu considero tudo aquilo que não está na pasta da engine, como sendo de fato a lógica do game.

### RUNNING THE GAME
Para rodar o game é simples, basta executar o comando para o script main.py ou equivalente em outros sistemas operacionais:
```
python main.py
```
desde que o main.py estaja na maior hierarquia dos scripts, o jogo deve rodar sem maiores problemas, `pygame` package é necessário.

<br>

## START SCREEN
Há um fun fact interessante, apesar do repositório ser chamado de Comets, o título do jogo ser Comets, dentro do código, estes corpos rochosos sempre foram tratados com o nome de Meteor.
![menu](https://user-images.githubusercontent.com/24737993/209238918-09eef8db-9879-4f26-9f18-8bad728e03f1.gif)

<br>

## GAME OVER SCENE & SCORE SCENE
Quando o jogador é morto, a scene atual é setada para a game_over_scene, esta por sua vez, conta alguns segundo para setar a cena atual como sendo a score_scene

Uma vez na score_scene, a scene é capaz de entender em que contexto foi setada, e ao perceber que um GameOver a setou como a current_scene no GameLoop, verifica os pontos marcados do player, e caso ele se qualifique, um ScoreRegistrationFloatingMenu é mostrado na scene, onde o player por ele, poderá ter sua pontuação registrada na score sheet juntamente com um nome de até 3 characteres.

### OVERVIEW
aikdujnasnd

### DETALHES DE IMPLEMENTAÇÃO
* são mostrados apenas os 10 primeiros elementos do arquivo CSV que guarda os nomes e os scores.
* este CSV é sorted toda vez que a score_scene é setada como a current_scene.
* toda a manipulação do CVS é feita com um sistema na engine chamado FileManager.

### VALIDAÇÃO DE REGISTRO:
* pontuação maior que 0.
* pontuação maior que o 10º elemento ou último elemento caso o CSV possua menos de 10 elementos.
* o nome inserido obrigatoriamente deve possuir 3 caracteres


