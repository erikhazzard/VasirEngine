import CairoPlot
import cairo
import math

#Function Plot
#test1
data = lambda x : math.sin(0.1*x)*math.cos(x)
CairoPlot.function_plot('function1', data, 800, 300, grid = True, dots = True, h_bounds=(0,80), step = 0.9, discrete = True)

#test2
CairoPlot.function_plot('function2', data, 800, 300, grid = True, h_bounds=(0,80), step = 0.9)

#test3
CairoPlot.function_plot('function3', data, 800, 300, grid = True, h_bounds=(0,80), step = 0.1)

#test4
data = lambda x : x**2
CairoPlot.function_plot('function4', data, 400, 300, grid = True, h_bounds=(-10,10), step = 0.1)

#Bar Plot
#test1
data = {'teste00' : [27], 'teste01' : [10], 'teste02' : [18], 'teste03' : [5], 'teste04' : [1], 'teste05' : [22], 'teste06' : [31], 'teste07' : [8]}
CairoPlot.bar_plot ('bar1', data, 400, 300, border = 20, grid = True, rounded_corners = False)

#test2
data = [3,1,10,2]
CairoPlot.bar_plot ('bar2.png', data, 300, 300, border = 20, grid = True, rounded_corners = True)

#test3
data = [[1.4, 3, 11], [8, 9, 21], [13, 10, 9], [2, 30, 8]]
h_labels = ["group1", "group2", "group3", "group4"]
colors = [(1,0.2,0), (1,0.7,0), (1,1,0)]
CairoPlot.bar_plot ('bar3', data, 500, 350, border = 20, grid = True, rounded_corners = False, h_labels = h_labels,colors = colors)
CairoPlot.bar_plot ('bar_rounded.png', data, 400, 300, border = 20, grid = True, rounded_corners = True, h_labels = h_labels, colors = colors)
CairoPlot.bar_plot ('bar_3D.png', data, 400, 300, border = 20, grid = True, three_dimension = True, colors = colors)

#test4
data = [[3,4], [4,8], [5,3], [9,1]]
v_labels = ["line1", "line2", "line3", "line4", "line5", "line6"]
h_labels = ["group1", "group2", "group3", "group4"]
CairoPlot.bar_plot ('bar4', data, 600, 200, border = 20, grid = True)
CairoPlot.bar_plot ('bar4_hLabels', data, 600, 200, border = 20, grid = True, h_labels = h_labels)
CairoPlot.bar_plot ('bar4_vLabels', data, 600, 200, border = 20, grid = True, v_labels = v_labels)
CairoPlot.bar_plot ('bar4_vLabels_hLabels', data, 600, 200, border = 20, grid = True, h_labels = h_labels, v_labels = v_labels)
        
#Dot Line Plot
#test1
data = {"john" : [-5, -2, 0, 1, 3], "mary" : [0, 0, 3, 5, 2], "philip" : [-2, -3, -4, 2, 1]}
h_labels = ["jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008"]
v_labels = ["jan/2008", "feb/2008", "mar/2008", "apr/2008", "may/2008"]
CairoPlot.dot_line_plot('dotline1', data, 250, 150, axis = True, grid = True)
CairoPlot.dot_line_plot('dotline1_dots', data, 400, 300, h_labels = h_labels, v_labels = v_labels, axis = True, grid = True, dots = True)

#Pie Plot // Donut plot
#test1
background = cairo.LinearGradient(300, 0, 300, 400)
background.add_color_stop_rgb(0,0.4,0.4,0.4)
background.add_color_stop_rgb(1.0,0.1,0.1,0.1)
data = {"john" : 700, "mary" : 100, "philip" : 100 , "suzy" : 50, "yman" : 50}
CairoPlot.pie_plot("pie1", data, 600, 400, background = background )

#test2
CairoPlot.donut_plot("donut1_background", data, 600, 400, background = background, gradient = True, inner_radius = 0.3)
CairoPlot.donut_plot("donut1_gradient", data, 600, 400, gradient = True, inner_radius = 0.3)
CairoPlot.donut_plot("donut1_shadow", data, 600, 400, gradient = False, shadow = True, inner_radius = 0.3)

#Gantt Chart
#test1
pieces = [(0.5,5.5) , [(0,4),(6,8)] , (5.5,7) , (7,8)]
h_labels = [ 'teste01', 'teste02', 'teste03', 'teste04']
v_labels = [ '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009', '0010' ]
colors = [ (1.0, 0.0, 0.0), (1.0, 0.7, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0) ]
CairoPlot.gantt_chart('gantt1', pieces, 500, 350, h_labels, v_labels, colors)


background = cairo.LinearGradient(300, 0, 300, 400)
background.add_color_stop_rgb(0,0.7,0,0)
background.add_color_stop_rgb(1.0,0.3,0,0)
data = {"john" : 700, "mary" : 100, "philip" : 100 , "suzy" : 50, "yman" : 50}
colors = [ (232.0/255, 118.0/255, 107.0/255), 
           (255.0/255, 150.0/255, 117.0/255),
           (255.0/255, 130.0/255, 154.0/255),
           (232.0/255, 107.0/255, 194.0/255),
           (240.0/255, 117.0/255, 255.0/255) ]
CairoPlot.pie_plot("pie_blog.png", data, 600, 400, background = background, gradient = True, shadow = True, colors = colors)


background = cairo.LinearGradient(300, 0, 300, 400)
background.add_color_stop_rgb(0,0,0.4,0)
background.add_color_stop_rgb(1.0,0,0.1,0)
colors = [ (73.0/255, 233.0/255, 163.0/255), 
           (80.0/255, 254.0/255, 228.0/255),
           (95.0/255, 255.0/255, 140.0/255),
           (75.0/255, 233.0/255, 73.0/255),
           (142.0/255, 255.0/255, 81.0/255) ]
CairoPlot.donut_plot("donut_blog.png", data, 600, 400, background = background, gradient = True, shadow = True, colors = colors, inner_radius = 0.3)

data = lambda x : math.sin(0.1*x)*math.cos(x)
CairoPlot.function_plot('function_blog.png', data, 1000, 400, grid = True, h_bounds=(0,80), step = 0.1)

