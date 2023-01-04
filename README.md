# Design Pattern Choices (Descent Order of Both Use and Importance)

## Subclass Sandbox

Used in the majority of the code for various reasons. Here are a few:

1. It allows for more organized code. 
If a method inside a parent class is designed to be a holder for the main subclass method
then the viewer can easily understand what certain components during the program
actually do.
```python
class ImageComponent{

    def image_drawer():
        # Prints Image
    
    def image_scroll():
        # Scrolls Image

    def executor():
        raise NotImplemented

}

class ImageComponentExecution(ImageComponent){

    def executor():
        image_drawer()
        image_scroll()
}
```
2. It's flexible. Inside the methods that are associated with the parent class
we can modify any variables inside into the subclass of our choosing in order to
create other simpler alternatives.

3. It is "spammable". 

## "Command" Parameter

One of the most obvious when it comes throughout for creating other menus between
each other as it allows dynamically mapped menus and flexible alternatives in cosmetic
and functional options.

```python
class FadeTransition:
    # FadeIn Function

class ButtonTransition(FadeTransition):
    # Transition made by clicking the button

class Play(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen, **kwargs):
        # Play Menu Button Function

class Options(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen, **kwargs):
        # Option Menu Button Function
       
class MenuOption(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen, **kwargs):
        # ...

class CharacterSelect(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen, **kwargs):
        # ...

class Song(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen, **kwargs):
        # ...

class Quit(ButtonTransition, FadeTransition):
    def execute(self, buttons, menu_mouse_pos, screen, **kwargs):
        # ...

```

## Event-Driven Programming and Game Loop

Another obvious choices when it comes to OOP, as it enables the important inputs 
to be used throughout programming like timer and KEYDOWN. 

## Type-Object and Flyweight

Two natural fits for this type of program as it allows for simpler and more effective
organization of variables and functions throughout the program. In my view, the difference 
is the fact that flyweight can use the same variables over and over while the type object just specifies
a parent class that can be used inside a subclass that can simplify the process of identifying
a determined type of object as a whole.


## Prototype

This utility of this design pattern is a bit more subtle as it requires a class
which complements every method necessary inside of the class in order to function.
In other words, it means that the class needs to have every variable from the initial class
in order to function. But thanks to the type-object design pattern, it allows this design
pattern to become more flexible, effective and efficient during the program.

```python
class Main(Entity):
    def __init__(self, var1, var2) -> None:
        super().__init__(var1, var2) 
    # default settings 
    def clone(self) -> Entity:
        return Main(self.var1, self.var2)


class Other(Entity):
    def __init__(self, var1, var2, var3) -> None:
        super().__init__(var1, var2)
        self.var3 = var3
    # extra variables for this entity
    def clone(self) -> Entity:
        return Other(self.var1, self.var2, self.var3)

class Spawner:
    def spawn_Entity(self, prototype):
        return prototype.clone()
```

## Update method

* Update() -> A smaller and simpler usage into this program that allows for reusage of the same
function over and over again throughout sprite entities. In this case, is used to transmit the basic animation
of the current sprite drawn.
* Customized Updates -> It allows for more personalized usages of animation transitions throughtout
entities. 

```python
    def update(self) -> bool:
        return self.move_sprite(0.4)
    # simpler update usage

    while True:
        if 1:
            self.update_animation(animation_update, 1)
        if 2:
            ...
    # more complex usage
```

## Double-Buffer

This one's usage is less effective than all of the others above as it allows for
better graphical processing, but without it not much of a different performance
upgrade. It is only used in order to set up the initial display flags of pygame. 

## Physics Engine

A simple collision effect implemented when the enemy target has more health than usual
as it retreats backwards when both rectangle objects collide.

## Design Patterns and Features Not Used

* **Observer Design Pattern**: Not prioritary as it allows for global notifications like
Achievements. Spent more time polishing the program and correcting some bugs.
* **Event Queue Design Pattern**: Another design feature that is useless considering that these
types of games don´t require a wait command for notes to be spawned (at least in this case).
* **Network Programming Feature**: Not implemented due to lack of planning.
* **ByteCode Feature**: Not necessary as the Prototype and List Reference Implementation
is more than enough to compensate for the Spawner Implementation.
* **Singleton Design Pattern:** A redundant design pattern as python already allows
for protected and global variables and classes.
* **State Machine Design Pattern:** A design pattern that could have been implemented
inside the AnimationTransitionComponent in order to make better transitions throughout
other animations.

## Bugs Found in the Final Release
* During sucessive retries, the counter does not start at 0. 
* Animation bugs due to the maybe due to the implementation and lack
of a State Machine.
* Some Image-Loading Bugs due to inability of repetition of names in
python lists.
* Performance Issues during Game when too much blit commands are
applied.

## Final Criticisms

Despite an overall good project (at least for alpha version), I do believe
that it felt a bit undercooked in both execution of concept and reusability
in code. There are some parts in the code that feel unfinished and feel like they
deserved to be reworked into something more worthwhile.
