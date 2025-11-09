from manim import *
import networkx as nx
import random
import numpy as np

class PreferentialAttachment(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a1a"

        # Intro Text
        self.show_intro()

        # Initialize Graph
        self.graph = nx.Graph()
        self.positions = {}
        self.node_mobjects = {}
        self.edge_mobjects = {}

        # Add Initial Nodes
        self.add_initial_nodes()

        # Show Legends
        self.show_legends()
        
        # Show Title Before Growth
        title = Text("Scale-Free Network Growth", font_size=36).to_edge(UP).shift(DOWN*0.5)
        subtitle = Text("Using Preferential Attachment", font_size=24, color="#888888").next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Growing Network
        for new_node in range(3, 20):
            self.add_node_with_preferential_attachment(new_node)
            self.update_node_colors()
            self.update_highest_degree_display()
            self.wait(0.2)
        
        # Fade out everything (Graph with legends)
        self.fade_out_graph()

        # Show Degree Distribution
        self.show_degree_distribution()

        # Fade Out Everything (Power Law)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

        # Conclusion
        self.show_conclusion()

    def show_intro(self):
        intro_text = Text("Hello everyone 😊", font_size=36)
        self.play(Write(intro_text))
        self.wait(1)
        self.play(FadeOut(intro_text))

        hook_text = Text("Imagine you're a new user on a social media platform.\nWho do you follow? Most likely, someone popular!\nThis simple behavior leads to a fascinating phenomenon:\nThe Preferential Attachment Model!", font_size=30)
        self.play(Write(hook_text))
        self.wait(2)
        self.play(FadeOut(hook_text))

        # Real-world Examples
        examples = Text("Real-World Examples: \nSocial Networks, Citation Networks, Neural Connections", font_size=30)
        self.play(Write(examples))
        self.wait(2)
        self.play(FadeOut(examples))

    def add_initial_nodes(self):
        initial_positions = [np.array([-2, 1, 0]), np.array([2, 1, 0]), np.array([0, -2, 0])]
        for i in range(3):
            self.graph.add_node(i)
            self.positions[i] = initial_positions[i]
            node_mob = self.create_node(initial_positions[i], YELLOW)
            self.node_mobjects[i] = node_mob
            self.play(GrowFromCenter(node_mob), run_time=0.3)

        # Connect Initial Nodes
        self.graph.add_edges_from([(0, 1), (1, 2), (2, 0)])
        for u, v in self.graph.edges:
            edge = Line(self.positions[u], self.positions[v], color=WHITE, stroke_width=2)
            self.edge_mobjects[(u, v)] = edge
            self.play(Create(edge), run_time=0.3)

    def create_node(self, position, color):
        node = Circle(radius=0.15, fill_opacity=0.8, color=color)
        node.move_to(position)
        return node

    def add_node_with_preferential_attachment(self, new_node):
        degrees = [self.graph.degree(n) + 1 for n in self.graph.nodes]
        probabilities = [deg / sum(degrees) for deg in degrees]
        chosen_node = random.choices(list(self.graph.nodes), weights=probabilities, k=1)[0]

        # Positioning the new node
        angle, radius = random.uniform(0, TAU), 3 + random.uniform(-0.7, 0.7)
        new_pos = np.array([radius * np.cos(angle), radius * np.sin(angle), 0])

        self.graph.add_node(new_node)
        self.graph.add_edge(new_node, chosen_node)
        self.positions[new_node] = new_pos

        new_node_mob = self.create_node(new_pos, YELLOW)
        edge = Line(self.node_mobjects[chosen_node].get_center(), new_node_mob.get_center(), color=WHITE, stroke_width=2)

        self.node_mobjects[new_node] = new_node_mob
        self.edge_mobjects[(new_node, chosen_node)] = edge

        self.play(GrowFromCenter(new_node_mob), Create(edge), run_time=0.3)

    def update_node_colors(self):
        colors = {1: YELLOW, 2: ORANGE, 3: RED, 4: PINK, 5: BLUE, 6: GREEN}
        for node, node_mob in self.node_mobjects.items():
            degree = self.graph.degree[node]
            new_color = colors.get(min(degree, max(colors.keys())), GREEN)
            self.play(node_mob.animate.set_color(new_color), run_time=0.2)

    def update_highest_degree_display(self):
        # Remove previous text (if it exists)
        if hasattr(self, "highest_degree_text"):
            self.remove(self.highest_degree_text)

        # Find the node with the highest degree
        highest_node, highest_degree = max(self.graph.degree, key=lambda x: x[1])

        # Create the updated text
        self.highest_degree_text = Text(f"Max Degree: {highest_degree}", font_size=28, color=GOLD)
        self.highest_degree_text.to_corner(UL)

        # Add the new text to the scene
        self.add(self.highest_degree_text)

  
    def show_legends(self):
        legend_texts = [
            ("New Node with degree 1", YELLOW),
            ("Moderate with degree 2", ORANGE),
            ("Growing Influence with degree 3", RED),
            ("Emerging Hub with degree 4", PINK),
            ("Highly Influential with degree 5", BLUE),
            ("Super Hub with degree 6 or 6+", GREEN),
        ]

        legend_group = VGroup(
            *[VGroup(Dot(color=color), Text(label, font_size=18).next_to(Dot(color=color), RIGHT, buff=0.3))
              for label, color in legend_texts]
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR)

        self.add(legend_group)

    def fade_out_graph(self):
        elements = VGroup(*self.node_mobjects.values(), *self.edge_mobjects.values())
        self.play(FadeOut(elements), run_time=1.5)

    def show_degree_distribution(self):
        axes = Axes(
            x_range=[0, 5, 1], y_range=[0, 10, 2],
            axis_config={"color": WHITE}
        ).scale(0.8)
        
        x_label = Text("log(Degree)", font_size=20).next_to(axes, DOWN)
        y_label = Text("log(Frequency)", font_size=20).next_to(axes, LEFT)
        
        degrees = [d for _, d in self.graph.degree()]
        degree_count = {d: degrees.count(d) for d in set(degrees)}

        points = [[np.log(d), np.log(c)] for d, c in degree_count.items() if d > 0 and c > 0]
        dots = VGroup(*[Dot(axes.c2p(x, y), color=YELLOW) for x, y in points])

        title = Text("Degree Distribution (Power Law)", font_size=24).to_edge(UP)
        self.play(Create(axes), Write(x_label), Write(y_label), Write(title))
        self.play(Create(dots))

        if len(points) > 1:
            x_vals, y_vals = zip(*points)
            m, b = np.polyfit(x_vals, y_vals, 1)
            line = Line(axes.c2p(min(x_vals), m * min(x_vals) + b), 
                        axes.c2p(max(x_vals), m * max(x_vals) + b), color=RED)
            self.play(Create(line))
        self.wait(2)

        self.play(FadeOut(axes), FadeOut(dots), FadeOut(line), FadeOut(title), FadeOut(x_label), FadeOut(y_label))
    def show_conclusion(self):
        conclusion_text = Text("We explored how nodes attach preferentially, leading to Scale-Free networks.", font_size=30)
        self.play(Write(conclusion_text))
        self.wait(3)
        self.play(FadeOut(conclusion_text))

        thank_you = Text("Thank you for watching! 👋", font_size=36)
        self.play(Write(thank_you))
        self.wait(2)
        self.play(FadeOut(thank_you))
