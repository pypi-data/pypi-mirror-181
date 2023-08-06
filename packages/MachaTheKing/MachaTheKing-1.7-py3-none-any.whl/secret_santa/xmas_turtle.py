import turtle
import conversation
import random
#import emoji

def abcdef():
        screen= turtle.Screen()
        turtle.title('name')
        screen.setup(width=1.0, height=1.0)
        screen.bgcolor('black')
        screen.tracer(0)

        tt = turtle.Turtle()
        tt.hideturtle()

        colors_pen = ['green', 'white', 'blue', 'yellow', 'pink', 'purple', 'violet', 'gray']
        colors_fill = ['green', 'blue', 'white', 'yellow', 'pink','purple', 'violet', 'gray']
        tt.speed('fastest')

        def gg():
                for i in range (16):
                        x, y = random.randrange (-350, 350), random.randrange (-230,230)
                        ttl= turtle.Turtle () # create a new pen
                        ttl.color(random.choice (colors_pen))
                        #x= '\U0001f600'
                        name = 'Marry Christmas \n Macha'
                        ttl.write(name,font=('chiller',95, 'italic bold'), align="center")
                        #ttl.penup() # up the pen
                        #tt1.goto(15,60)
                        #tt1.pendown()
                        #ttl.write('Marry Christmas \n marry christmas',font=('chiller',60, 'italic bold'))
                        ttl.clear()
                        tt.penup() # up the pen
                        tt.goto(x,y) # 
                        tt.pendown() #down the pen
                        tt.begin_fill() # ar
                        tt.color(random.choice (colors_fill))
                        for i in range(6): 
                            tt.forward(36)
                            tt.right(144)
                        tt.end_fill() # 

        for _ in range(10): 
            gg()
            tt.clear() # clear the tt pen (stars)

        
            

        tt.clear()
        turtle.bye()
        return 'Done'
        
        #turtle.mainloop()


if __name__ ==  '__main__':
        abcdef()
