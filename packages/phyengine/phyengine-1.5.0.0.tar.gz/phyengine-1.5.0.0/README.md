# **About**

This library can help you program some simple kinematics processes and get some important (maybe) data from it

# **Getting saterted**

## **Installing**
To install phyengine, run following command in command prompt:

```
pip install phyengine
```

## **Importing**

You can use ususal import

```
import phyengine
```

# **phyengine.MathEngine**

## **Vectors**

Phyengine can work with 2d vectors. General syntax to create vector object is

```
phyengine.MathEngine.Vector(coordx: float, coordy: float)
```

For example:

```
first = phyengine.MathEngine.Vector(2, 3)
```

To get coord of vector, try this:

```
print(first.x)
print(first.y)

# Output:
# 2
# 3
```

Also, you can print vector:

```
print(first)

# Output:
# Vector object with coords (2, 3)
```

### **Operations with vectors**

**Addition/Substracting**

```
a = phyengine.MathEngine.Vector(2, 3)
b = phyengine.MathEngine.Vector(3, -7)

res1 = a + b
res2 = a - b
print(res1)
print(res2)

# Output:
# Vector object with coords (5, -4)
# Vector object with coords (-1, 10)
```

**Multiplying/Dividing vector by int/float**

```
a = phyengine.MathEngine.Vector(5, 6)
b = 1.2
c = 2

res1 = a * b
res2 = a / c
print(res1)
print(res2)

# Output:
# Vector object with coords (6, 7.2)
# Vector object with coords (2.5, 3)
```

**Iterating by vector**

Iterating by vector is equal to iterating by tuple (vector.x, vector.y)

```
a = phyengine.MathEngine.Vector(5, 6)

for i in a:
    print(i)

# Output:
# 5
# 6
```

**Getting absolute value of vector**

Absolute value of vector is calculated as sqrt(vector.x^2 + vector.y^2)

```
a = phyengine.MathEngine.Vector(3, 4)

print(abs(a))

# Output:
# 5
```

**Getting unit vector**

Unit vector is a vector, which absolute value is 1 and has the same direction as given

```
a = phyengine.MathEngine.Vector(3, 4)

e = a.unit
print(e)

# Output:
# Vector object with coords (0.6, 0.8)
```

**Getting zero Vector**

You can get vector with coords (0, 0) by using Vector.ZERO()

```
print(Vector.ZERO())

# Output:
# Vector object with coords (0, 0)
```

# **phyengine.InputManager**

InputManager can help you get data from keyboard to control your simulation.
To init Input, you need to run this:

```
phyengine.InputManager.init(*args)
```

where *args - list of buttons, that you want to record. For example:

```
input_ = phyengine.InputManager.init("space", "q", "w")
``` 

### **Operations with input**

**Getting if button is held**

```
input_.held(key)
```

Will return true while buttons with name "key" is pressed

**Getting if button was pressed**

```
input_.pressed(key)
```

Will return true only when button with name "key" was pressed first time

# **phyengine.MainEngine**

This is main part of phyengine. It allows to create windows and add objects on it

## **BasicWindow**

This class create a new window. General syntax is

```
phyengine.MainEngine.BasicWindow(width: int, height: int, ping: int = 30, scale: float = 10)
```

where width, height - width and height of window in pixels, ping - time in ms between to window redraws (the more ping is - the more stable window is but less smooth it is), scale shows how much screen pixels are in one imaginary meter.

For example

```
window = phyengine.MainEngine.BasicWindow(600, 600, 12, 85)
```

You can get this parameters as window.x, window.y, window.ping and window.scale:

```
window = phyengine.MainEngine.BasicWindow(600, 600, 12, 85)
print(window.x, window.y, window.ping, window.scale, sep='\n')

# Output:
# 600
# 600
# 12
# 85
```

### **Working with window**

**Activating window**

After creating window, you won't see anything. You need to add window.start() to see it

```
window = phyengine.MainEngine.BasicWindow(600, 600, 12, 85) #Nothing will happen
window.start() #Now you will be able to see window
```

**Setting update function**

update function will call every window redraw. To create it, you need to write a function, that takes 0 arguments and make window.update equal to it:

```
window = phyengine.MainEngine.BasicWindow(600, 600, 12, 85)
def w_update():
    print("Screen was redrawed!")
window.update = w_update
```

This code will print text every 12 ms, because window.ping equals to 12

**Getting window working time**

You can get window working time (in imaginary seconds) by window.time (Imaginary seconds can not be the same as real, because it take some time to call update function, e.t.c):

```
window = phyengine.MainEngine.BasicWindow(600, 600, 12, 85)
window.update = lambda: print(window.time)
window.start()
```

**Getting list of window objects**

window.Objects return list of DynamicObjects on this screen. DynamicObject clss will be explained below

**Resume/pause window**

window.pause() and window.resume() can pause/continue all processes in window. By default it is possible to click on window and phyengine will automaticly pause/resume it (if window is paused, it will resume it and if window is resumed, it will pause it)

## **DynamicObject**

Dynamic object class allows to create objects on window. General syntax is

```
phyengine.MainEngine.DynamicObject(window: phyengine.MainEngine.BasicWindow, x: float, y: float, collidable: bool = True, image: phyengine.DynamicObjectManager.DO_Image = phyengine.DynamicObjectManager.DO_Image.STANDART(), behaivour: phyengine.DynamicObjectManager.DO_Behaivour = phyengine.DynamicObjectManager.DO_Behaivour.STANDART())
```

where window - window, in which you want to place object, x, y - start coords of object, collidable sets the ability of object collide with other (will be explained below), image sets shape of object, behaivour sets how object will behave (gravity, air friction, e.t.c). image and behaivour will be explained below, in chapter phyengine.DynamicObjectManager

All of this variables you can get by using object_.x, object_.y, object_.window e.t.c

IMPORTANT. Coords of object are measured from upper left corner of window!!!

For example

```
window = phyengine.MainEngine.BasicWindow(600, 600, 12, 85)
object_ = phyengine.MainEngine.DynamicObject(window, 300, 300)
window.start()
```

### **Working with DynamicObject**

**Setting update function**

It is very similiar to window update - you need to create function that takes 0 arguments and make object_.update equal to it and it will be called every window redraw

```
window = phyengine.MainEngine.BasicWindow(600, 600, 12, 85)
object_ = phyengine.MainEngine.DynamicObject(window, 300, 300)
object_.update = lambda: print(object_.x, object_.y)
window.start()
```

**Getting window ping from object**

object_.dt will return time in s between two window redraws. So, object_.dt equals to window.ping / 1000

**Move object**

You can use object_.move(dx, dy) to move object by dx pixels right and dy pixels down

**Setting position, velocity and acceleration**

You can set position of object by using object_.position = phyengine.MathEngine.Vactor(new_x, new_y) or other iterable object (tuple, list, e.t.c) and object will move to coords (new_x, new_y)

You can set velocity of object by using object_.speed = phyengine.MathEngine.Vactor(v_x, v_y) (For veclocity and acceleration you can not use not Vector object!!!!) and every imaginary second object will move for (v_x, v_y) imaginary meters (not pixels)

You can get acceleration of object by using object_.acceleration = phyengine.MathEngine.Vactor(a_x, a_y)) and every imaginary second object velocity will be increased for (a_x, v_y) imaginary meters (without gravity and air friction)

You can get position, velocity and acceleration using object_.position, object_.speed and object_.acceleration

**Getting colision with other object**

If there are more than two object on screen, you can use object_.collide_with(other), where other - it is second DynamicObject to check colision between them. If other.collidable == False or object_.collidable == False, it will return False

IMPORTANT. It is no action by default on colision. You need to set it by yourself

TIP. You can use object_.collide_with_borders() to know if object collide with borders

**Equation between to object**

Every object has it's unique index. You can get it by object_.index. If index of two objects are the same, objects are equal to each other

**Stamp object**

object_.stamp(color) will create 2x smaller image of object with "color" fill in a place, where object is placed now

# **DynamicObjectManager**

This module allows to create image or behaivour of DynamicObject as class

## **DO_Image**

This class sets shape of DynamicObject. You can create this as

```
phyengine.DynamicObjectManager.DO_Image(shape_type: str = 'circle', **kwargs)
```

shape_type can be 'circle' or 'rectangle'. Also, neccesary part is color argument, that sets color of future DynamicObject. Also, by using image.dx and image.dy you can get semi-width and semi-height of DynamicObject, where image - object of DO_Image class

### **shape_type = 'circle'**

In this case, neccesary arguments are:
d - diameter of circle in pixels (not imaginary meters!)

For example

```
image = phyengine.DynamicObjectManager.DO_Image('circle', d = 20, color = 'gold')
print(image.dx)
print(image.dy)

# Output:
# 10
# 10
```

### **shape_type = 'rectangle'**

In this case, neccesary arguments are:
width - width of rectangle in pixels (not imaginary meters!), 
height - height of rectangle in pixels (not imaginary meters!)

For example

```
image = phyengine.DynamicObjectManager.DO_Image('rectangle', width = 20, height = 30, color = 'gold')
print(image.dx)
print(image.dy)

# Output:
# 10
# 15
```

### **Standart DO_Image**

phyengine.DynamicObjectBehaivour.DO_Image.STANDART() will return image of circle with diameter of 10 pixels with red fill

## **DO_Behaivour**

This class allows to set behaivour of DynamicObjects. General syntax is

```
phyengine.DynamicObjectManager.DO_Behaivour(bounce_from_borders_friction: float = -1, gravity: float = -1, air_friciton: float = -1)
```

where bounce_from_borders_friction set proportion between energy before colision with borders and after it (for example, if bouce_from_borders == 0.5 that means that saved energy after colision will be 2x less than energy before it is), gravity sets proportion between gravity force and 'mass' of objects (free fall acceleration), air_frcition sets proportion between velocity square and air friction acceleration. You can get this values as behaivour.bounce_from_borders_friction, behaivour.gravity and behaivour.air_friction

IMPORTANT. If variables are less that zero, they doesn't affect on behaivour (if gravity < 0, object will not fall, e.t.c)

### **Standart behaivour**

phyengine.DynamicObjectManager.DO_Behaivour.STANDART() will return behaivour with no bounce_from_borders, no gravity and no air_friction

# **DataEngine**

DataEngine can help to work with files (for example, create file with recorded data modelation)

## **RecordableValue**

RecordableValue is a class that can check some data from modelation and save it in .txt or .xlsx file.
General syntax is 

```
value = phyengine.DataEngine.RecordableValue(x_expression: str = "0", y_expression: str = "0", window = None, **kwargs)
```

where x_expression/y_expression is a expression for x/y axis of data (for example, to create plot in future (x axis can be time or another argument, y is dependent value)), window is a window value is attended to (data will be recorded every window redraw), **kwargs are some named srguments that are needed to eval expression. For example:

```
window = phyengine.MainEngine.BasicWindow(600, 600, 12, 85)
object_ = phyengine.MainEngine.DynamicObject(window, 300, 300)
value = phyengine.DataEngine.RecordableValue("wi.time", "pl.speed.y", window, pl = object_, wi = window)
```

While evaluating, phyengine will replace every 'wi' in expression with window object with window, every 'pl' with object_ e.t.c

### **Operations with recordable value**

**Saving**

You can save file in .txt or .xlsx format using value.save(name, file_type). Name is an argument that show name of future file (For example, 'some_recorded_data'), file_type can be phyengine.DataEngine.TXT or phyengine.DataEngine.EXCEL and show type of future file.

**Differentiation**

By using value.differentiate(index) you can get APPROXIMATION of index value of differentiation of y_expression of value (index numeration starts from 0)