# COMETS

link: https://github.com/JNetoGH/Comets

## ALUNOS
João Neto (a22200558):
- desenvolvimento da game engine
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

<br>

<br>

## GAME-ENGINE (quick overview)

#### ENGINE VS JOGO EM MINHA ARQUITETURA
O jogo está separado em pastas, há pastas exclusivas da JNeto Productions Game Engine, esta é uma ferramenta discreta, o jogo em si, é composto por GameObjects, os quais não ficam localizados juntamente da engine, porém, acessam seus recursos, tais quais, Systems, GameLoop, Components, Scenes, Prefabs, RenderingLayers e Cameras.

Com isso em mente, eu considero tudo aquilo que não está na pasta da engine, como sendo de fato a lógica do game.

#### RUNNING THE GAME
Para rodar o game é simples, basta executar o comando para o script main.py ou equivalente em outros sistemas operacionais:
```
python main.py
```
desde que o main.py esteja na maior hierarquia dos scripts, o jogo deve rodar sem maiores problemas, `pygame` package é necessário.

<br>

<br>

<br>

## GAMEPLAY
https://user-images.githubusercontent.com/24737993/209355125-e6550c08-7325-4419-949c-bf7fe69db374.mp4

<br>

<br>

<br>

## START SCREEN
Há um fun fact interessante, apesar do repositório ser chamado de Comets, o título do jogo ser Comets, dentro do código, estes corpos rochosos sempre foram tratados com o nome de Meteor.
![menu](https://user-images.githubusercontent.com/24737993/209238918-09eef8db-9879-4f26-9f18-8bad728e03f1.gif)

<br>

<br>

<br>

## CÂMERA
A câmera da scene principal do game possui 2 estados, fixa ou seguindo jogador, o player pode mudar o estado pressionando a tecla `P`.

![camera](https://user-images.githubusercontent.com/24737993/209357547-23e83e27-829d-4834-8f2f-7f433586a8fe.gif)

<br>

<br>

<br>

## ROTATION, MOVEMENT, DIRECTION AND SHIP INERTIA
Não existe freio automático, a nave possuí inércia, uma força contrária é feita para desacelerar o player, esta força leva um certo tempo até deixar a nave e ponto morto.

A nave não sai de 0 a velocidade máxima instantaneamente, uma força de é aplicada na direção em que a nave esta "facing", causando aceleração, esta força leva um certo tempo para acelerar a nave até a sua velocidade máxima.

````
def game_object_update(self) -> None:

    # GENERATES THE FORWARD MOVE DIRECTION
    self._generate_direction_from_ship_angle()

    # MOVEMENT
    # moves forward when W or UP arrow is pressed
    if InputManager.Vertical_Axis == -1:
        self._accelerate()
        self._move_player_forward()
    elif self.current_speed > 0:
        self._decelerate()
        self._move_player_forward()

    # ROTATION
    # rotates player according to A, D, < adn >keys
    if InputManager.Horizontal_Axis != 0:
        self._rotate_player()
````
![movement](https://user-images.githubusercontent.com/24737993/209372490-d6d0fff4-32ab-48f9-84e7-95176e360a47.gif)

<br>

<br>

<br>

## SHOOTING
- um disparo é gerado ao pressionar `SPACE`, tendo este a mesma direção em que o player estava rotacionado.
- os disparos possuem uma cadência com 1 segundo de intervalo (obrigatório pelo professor).
- há uma barra lateral que indica o tempo do intervalo, quando cheia, pode-se disparar novamente.
- cada disparo tem uma vida útil de 4 segundos (obrigatório pelo professor), após esse período, o disparo é manejado para garbage collection.
- caso o CircleTriggerComponent de um Meteor colida com um disparo, o disparo e o Meteor são manejados para garbage collection.

![shooting](https://user-images.githubusercontent.com/24737993/209375643-bf780ed4-157b-4544-8758-982bcd41a552.gif)

<br>

<br>

<br>

## COMETS or METEORS or ASTEROIDS

- Os Cometas são manejados por um GameObject chamdo MeteorManager.
- A quantidade máxima de cometas na scene depende da dificuldade atual (é progressiva, varia de acordo com a altura da gameplay).
- A direção do spawn de um Meteor é decidida pleo MeteorManager de forma a que o meteoro sempre passe pelo mapa.
- Os cometas possuem uma vida útil de mais ou menos meio minuto, ao fim da vida útil, aquele cometa é manejado para garbage collection.
- Quando o CircleTriggerComponent colide com o player ou um disparo, este cometa é manejado para garbage collection.

- Quando o MeteorManager spawna um cometa, o mesmo tem as seguintes chances de ser um:
    
    - Cometa Grande -> 20%
    - Cometa Médio -> 30%
    - Cometa Pequeno -> 50%

    ```
    rank = None
    rank_picker = random.randint(1, 10)
    if 1 <= rank_picker <= 5:
        rank = Meteor.MeteorRank.Small
    elif 6 <= rank_picker <= 8:
        rank = Meteor.MeteorRank.Mid
    elif rank_picker <= 10:
        rank = Meteor.MeteorRank.Big
    ```

- Cada cometa destruído dá uma pontuação diferente:

    - Cometa Grande -> 10 pontos
    - Cometa Médio -> 20 pontos
    - Cometa Pequeno -> 30 pontos

- Quando um cometa é atingido por uma bala dependendo do seu tipo, pode multiplicar-se em cometas de um tipo abaixo, ou seja:

    - Cometa Grande -> 3 x Cometa Medio
    - Cometa Médio -> 5 x Cometa Pequeno
    - Cometa Pequeno -> Destroy

<br>

<br>

<br>

## GAME OVER SCENE & SCORE SCENE
Quando o jogador é morto, a scene atual é setada para a game_over_scene, esta por sua vez, conta alguns segundo para setar a cena atual como sendo a score_scene.

Uma vez na score_scene, a scene é capaz de entender em que contexto foi setada, e ao perceber que um GameOver a setou como a current_scene no GameLoop, verifica os pontos marcados do player, e caso ele se qualifique, um ScoreRegistrationFloatingMenu é mostrado na scene, onde o player por ele, poderá ter sua pontuação registrada na score sheet juntamente com um nome de até 3 characteres.

#### PREVIEW
https://user-images.githubusercontent.com/24737993/209350149-feb5d8c9-b841-4544-bcb5-ef5e334f81c1.mp4

#### DETALHES DE IMPLEMENTAÇÃO
* são mostrados apenas os 10 primeiros elementos do arquivo CSV que guarda os nomes e os scores.
* este CSV é sorted toda vez que a score_scene é setada como a current_scene.
* toda a manipulação do CVS é feita com um sistema na engine chamado FileManager.

#### VALIDAÇÃO DE REGISTRO:
* pontuação maior que 0.
* pontuação maior que o 10º elemento ou último elemento caso o CSV possua menos de 10 elementos.
* o nome inserido obrigatoriamente deve possuir 3 caracteres.

<br>

<br>

<br>

## PROGRESSIVE DIFFICULTY
Uma solução simples e elegante para uma dificuldade progressiva neste jogo foi, diminuir a duração do intervalo com que o MeteorManager instancia os meteoros com base na pontuação atual do player.

- o tempo de intervalo inicial é de 0.75 sec.
- há um cap de 0.3 sec de tempo de intervalo mínimo (a.k.a. dificuldade máxima), quando chega nele, a dificuldade para de aumentar.
- há uma barra lateral na direita que indica a dificuldade atual do jogo:

![dificuldades](https://user-images.githubusercontent.com/24737993/209385988-618fe309-4684-44d3-8b66-0dcfad977fe0.png)


<br>

<br>

<br>

## SOUNDS
O game possui som para todos os lados, eu utilizei uma coleção de efeitos sonoros, um asset pessoal que comprei na Unity Asset Store, não havendo assim nenhum problema legal de copyright.

#### SONS USADOS

![image](https://user-images.githubusercontent.com/24737993/209388309-89931976-ea66-46ad-bc0e-6c50a2716288.png)


#### ASSET 
https://assetstore.unity.com/packages/audio/music/orchestral/total-music-collection-89126
