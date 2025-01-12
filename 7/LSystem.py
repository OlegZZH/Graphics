import turtle

def apply_rules(ch, rules):
    return rules.get(ch, ch)

def generate_l_system(axiom, rules, iterations):
    result = axiom
    for _ in range(iterations):
        result = ''.join(apply_rules(ch, rules) for ch in result)
    return result

def draw_l_system(turtle, instructions, angle, distance):
    for instruction in instructions:
        if instruction == 'F':
            turtle.forward(distance)
        elif instruction == '+':
            turtle.left(angle)
        elif instruction == '-':
            turtle.right(angle)

def main():
    axiom = "X"
    rules = {'X': 'XFYFX+F+YFXFY-F-XFYFX',"Y":"YFXFY-F-XFYFX+F+YFXFY"}
    angle = 90
    iterations = 6
    distance = 5

    l_system = generate_l_system(axiom, rules, iterations)

    # Create turtle
    window = turtle.Screen()
    window.bgcolor("white")
    window.title("L-System Fractal")

    fractal_turtle = turtle.Turtle()
    fractal_turtle.speed(0)

    fractal_turtle.penup()
    fractal_turtle.goto(0, -150)
    fractal_turtle.pendown()

    draw_l_system(fractal_turtle, l_system, angle, distance)

    window.mainloop()

if __name__ == "__main__":
    main()
