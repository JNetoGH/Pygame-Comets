# COMETS
link: https://github.com/JNetoGH/comets

<br>

<br>

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

<br>

<br>

## GAME-ENGINE (quick overview)

#### ENGINE VS JOGO EM MINHA ARQUITETURA
O jogo está separado em pastas, há pastas exclusivas da JNeto Productions Game Engine, esta é uma ferramenta discreta, o jogo em si é composto por GameObjects, os quais não ficam localizados juntamente da engine, porém, acessam seus recursos, tais quais, Systems, GameLoop, Components, Scenes, Prefabs, RenderingLayers e Cameras.

Com isso em mente, eu considero tudo aquilo que não está na pasta da engine, como sendo de fato a lógica do game.

#### RUNNING THE GAME
Para rodar o game é simples, basta executar o comando para o script main.py ou equivalente em outros sistemas operacionais:
```
python main.py
```
desde que o main.py estaja na maior hierarquia dos scripts, o jogo deve rodar sem maiores problemas, `pygame` package é necessário.

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
Não exite freio automático, a nave possuí inércia, uma força contrária é feita para desacelerar o player, esta força leva um certo tempo até deixar a nave e ponto morto:

![movement](https://user-images.githubusercontent.com/24737993/209372490-d6d0fff4-32ab-48f9-84e7-95176e360a47.gif)

#### CODES
- ROTATION: a Rotatção é simples de se entender, uma angular_velocity é responsável por determinar o quanto de incremento/decremento o ângulos usado pra rotacionar a nave terá naquele frame, consoante aos inputs do player: (`<`, `>`) ou (`A`, `D`)
    ```
    def _rotate_player(self):

        # increments(A/<)/decrements(D/>) the angle according to angular speed
        self.angle = self.angle + self.angular_velocity * GameTime.DeltaTime if InputManager.Horizontal_Axis == -1 else self.angle
        self.angle = self.angle - self.angular_velocity * GameTime.DeltaTime if InputManager.Horizontal_Axis == 1 else self.angle

        # it's not really necessary, it works with a 7232º, but I prefer keeping it in the ]0º, 360º] for visualization
        self.angle = self.angle = 0 + (self.angle - 360) if self.angle > 360 else self.angle  # 0   + oq passou de 360
        self.angle = self.angle = 360 - (self.angle * -1) if self.angle < 0 else self.angle   # 360 - oq passou de 0

        # rotates keeping the buffered image as it its
        self.image = pygame.transform.rotate(self.buffered_original_image, self.angle)
    ```

- DIRECTION: a direção, é feita a partir do angulo atual do player:
    ````
    def _generate_direction_from_ship_angle(self):

        # I need to add/sub more 180 because my default orientation for 0 is ↑ sited of 0º aiming ↓ by default
        angle_in_rad = math.radians(self.angle-180)

        # makes the direction, normalizing can't throw a division by 0 exception, because a (0,0) direction is impossible
        self.dir_from_angle = pygame.Vector2(math.sin(angle_in_rad), math.cos(angle_in_rad)).normalize()
    ````

- INERTIA: eu usei como base o que já conhecia para desaceleração com resistência do ar, como no espaço não existe ar, podemos chamar de "força contrária dos motores dianteiros" ou algo do gênero XD, ela atua diretamente na velocidade do objeto, incrementando/decrementando:
    ````
    def _accelerate(self):
        self.current_speed = self.current_speed + (self.ACCELERATION * GameTime.DeltaTime)
        if self.current_speed > self.BASE_MAX_MOVE_SPEED:
            self.current_speed = self.BASE_MAX_MOVE_SPEED

    def _decelerate(self):
        self.current_speed = self.current_speed - (self.DECELERATION * GameTime.DeltaTime)
        if self.current_speed < 0:
            self.current_speed = 0
    ````

- MOVEMENT: O movimento é o clássico:
    ```
        def _move_player_forward(self):
            new_position = self.transform.world_position_read_only + self.dir_from_angle * self.current_speed * GameTime.DeltaTime
            self.transform.move_world_position_with_collisions_calculations(new_position)
    ```

<br>

<br>

<br>

## GAME OVER SCENE & SCORE SCENE
Quando o jogador é morto, a scene atual é setada para a game_over_scene, esta por sua vez, conta alguns segundo para setar a cena atual como sendo a score_scene

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
* o nome inserido obrigatoriamente deve possuir 3 caracteres


