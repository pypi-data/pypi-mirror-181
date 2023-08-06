get_ipython().run_line_magic('matplotlib', 'widget')
import matplotlib

from IPython.display import display
import ipywidgets as widgets
from tkinter import Tk
from tkinter import filedialog
from vaxm import VAX
import numpy as np
from tkinter import messagebox
import matplotlib.pyplot as plt











porder = vorder = coverage = range_frame = left = right = top = bottom = None

output = widgets.Output()

jeps_vis = display( display_id = 'jeps_vis' )
maps_vis = display( display_id = 'maps_vis' )
tooltip_vis = display( display_id = 'tooltip_vis' )

file_name_ = ''
dtm = exp = patterns = None
X_emb_ = y_ = x_name_ = None
fig = ax = None











def open_file_f( b ):
    global file_name_, jeps_vis, dtm
        
    
    Tk().withdraw() 
    file_name = filedialog.askopenfilename( title = 'Open VAX csv file ...', initialdir = './', filetypes = [ ( 'VAX csv file', '*.csv' ) ] )

    if file_name_ != '':

        file_name_ = file_name.replace( '.csv', '' )            
        jeps_vis.update( 'JEPs' )

        dtm = None
        jeps()
        
        

        
        






def jeps():
    global porder, vorder, coverage, range_frame, left, right, top, bottom, dtm, exp, patterns
    
        
    if dtm == None:        
        dtm = VAX( verbose = 0 )
        dtm.load( file_name_ )
    
    r_order = 'raw'
    if porder.label != 'none': r_order = porder.label
    
    f_order = 'raw'
    if vorder.label != 'none': f_order = vorder.label
        
    draw_range_box = range_frame.value
    
    margin_left = left.value
    margin_right = right.value
    margin_top = top.value
    margin_bottom = bottom.value
        
        
        
    if ( patterns is not None ) and ( len( patterns ) == 0 ):
        
        jeps_vis.update( '< JEPS >, Select an instance or Reset.' )
        
    else:
    
    
        # try:



        if patterns is None: # start and reset

            exp = dtm.explanation( r_order = r_order, f_order = f_order, draw_distribution = True, show_feature_importance = True, show_info_text = False ) # r_order starts with 'support'

            patterns = exp.rules_[ :2 ].tolist() # the 2 highest support patterns

            coverage.value = ( dtm.rules_matrix_[ patterns[ 0 ], dtm.COVERAGE ] + dtm.rules_matrix_[ patterns[ 1 ], dtm.COVERAGE ] + 0.01 ) * 100

            exp = dtm.explanation( rules = np.array( patterns ) + 1, f_order = f_order, draw_distribution = True, show_feature_importance = True, show_info_text = False )

        else:

            if coverage.disabled == False:

                data_coverage_max = coverage.value / 100.00

                exp = dtm.explanation( r_order = r_order, f_order = f_order, data_coverage_max = data_coverage_max, draw_distribution = True, show_feature_importance = True, show_info_text = False )

                patterns = exp.rules_.tolist()

            else:

                exp = dtm.explanation( rules = np.array( patterns ) + 1, r_order = r_order, f_order = f_order, draw_distribution = True, show_feature_importance = True, show_info_text = False )

                patterns = exp.rules_.tolist()



        exp.create_svg( draw_range_box = draw_range_box, margin_left = margin_left, margin_right = margin_right, margin_top = margin_top,  margin_bottom = margin_bottom, draw_row_labels = True, draw_rows_line = False, draw_col_labels = True, draw_cols_line = False, col_label_degrees = 12, cell_background = 'all', cell_background_color = '#f2f2f2', rows_left_legend_show_value = True, draw_box_frame = False, stroke = '#000000', inner_pad_row = 5, inner_pad_col = 5, draw_box_row_left_legend = True, draw_frame_left_legend = False, draw_frame_right_legend = False, draw_box_row_right_legend = False, draw_frame_top_legend = False, rows_right_legend_width = 75/3, binary_legend = [ '< 0.05', '>= 0.05' ], matrix_legend_ratio = 0.75 )

        jeps_vis.update( exp.display_jn() )


        
        # except Exception as e:

        #     Tk().withdraw() 
        #     messagebox.showinfo( "Error",  str( e ) )







        

        
        
def on_pick( event ):
    global coverage, dtm, patterns, x_name_
    with output:

    
        if event.mouseevent.button == 1:
            
        
            if( coverage.disabled == False ):

                coverage.disabled = True
                coverage.value = 0.0

            p = dtm.instances_map_[ :, event.ind[ 0 ] ].nonzero()[ 0 ][ 0 ]
            
            if p not in patterns:
                
                patterns.append( p )
                
                if( x_name_ is not None ):
                    tooltip_vis.update( x_name_[ event.ind[ 0 ] ] + ', pattern p' + str( p + 1 ) )
            else:
                
                patterns.remove( p )
                
                if( x_name_ is not None ):
                    tooltip_vis.update( '< >' )

            jeps()
            maps()
            
            
        elif event.mouseevent.button == 3:
            
            
            p = dtm.instances_map_[ :, event.ind[ 0 ] ].nonzero()[ 0 ][ 0 ]
            
            tooltip_vis.update( 'Pattern ' + str( p + 1) + ': ' + np.array2string( x_name_[ dtm.instances_map_[ p, : ].nonzero()[ 1 ] ], separator = ',' ) )






        
        
    


def maps():
    global dtm, patterns, X_emb_, y_, fig, ax
    
    
    if( fig is None ) and ( ax is None ):
        
        fig, ax = plt.subplots( nrows = 1, ncols = 2, figsize = ( 9.5, 3 ) )
        
    else:
        
        ax[ 0 ].clear()
        ax[ 1 ].clear()
        
    
    fig.canvas.toolbar_visible = False
    fig.canvas.header_visible = False
    fig.canvas.footer_visible = False
    fig.canvas.callbacks.connect( 'pick_event', on_pick )
    
    
    ss = 6
    if len( patterns ) < ss: patterns_s = patterns
    else: patterns_s = patterns[ :ss ]
    
    
    dtm.plot_map( X_emb_, y_, np.array( patterns_s ), plt, fig, ax, font_legend_size = 8, size = 30, linewidth = 0.45, color_map1 = np.array( [ '#f2f2f2ff', '#1f77b3', '#ff7e0e', '#bcbc21' ] ), color_map2 = np.array( [ '#f2f2f2ff', '#e277c1', '#9367bc', '#bc0049', '#00aa79', '#ffdb00', '#d89c00', '#e41a1c', '#8c564b', '#ff9a75' ] ) )
    
    
    # plt.ioff()
    plt.tight_layout()
    # plt.show()






            
        

        
        
def save_figures_f( b ):
    global exp, fig

        
    Tk().withdraw() 
    file_name_s = filedialog.asksaveasfilename( title = 'Save figures ...', initialdir = './', filetypes = [ ( 'PNG', '*.png' ), ( 'SVG', '*.svg' ) ] )

    if file_name_s != '':

        img_type = file_name_s[-3:]            
        file_name_s = file_name_s.replace( '.' + img_type, '' )

        if img_type == 'png':

            exp.save( file_name_s + '-JEPs.png', pixel_scale = 5 )

            if( X_emb_ is not None ) and ( y_ is not None ):
                fig.savefig( file_name_s + '-MAPs.png', dpi = 300, bbox_inches = 'tight' )

        elif img_type == 'svg':

            exp.save( file_name_s + '-JEPs.svg' )
            if( X_emb_ is not None ) and ( y_ is not None ):
                fig.savefig( file_name_s + '-MAPs.svg', bbox_inches = 'tight' )

 



     
    
    
    


def order_filter_f1( change ): # update jeps
    jeps()
    
    
def order_filter_f2( change ): # update jeps and maps    
    jeps()    
    if ( X_emb_ is not None ) and ( y_ is not None ):
        maps()





        
        
        
        
        
def reset_f( b ):
    global porder, vorder, coverage, patterns

    
    porder.value = 2 # if 'porder.value' change, 'order_filter_f1()' will be called, and by that, 'jeps()'   
    vorder.value = 2 # if 'vorder.value' change, 'order_filter_f1()' will be called, and by that, 'jeps()'
    
    patterns = None        
    if ( x_name_ is not None ): tooltip_vis.update( '< >' )
    
    coverage.value = 0.0 # if 'coverage.value' change, 'order_filter_f2()' will be called, and by that, 'jeps()'
    if coverage.disabled == True: coverage.disabled = False
        
    range_frame.value = False





    
        
    
    
    

def vax_app( file_name = None, X_emb = None, y = None, x_name = None ):
    global porder, vorder, coverage, range_frame, left, right, top, bottom, file_name_, dtm, exp, patterns, X_emb_, y_, x_name_, fig, ax



    porder = vorder = coverage = range_frame = left = right = top = bottom = None

    file_name_ = ''
    dtm = exp = patterns = None
    X_emb_ = y_ = x_name_ = None
    fig = ax = None
    


    open_file = widgets.Button( description = "Open File" )
    save = widgets.Button( description = "Save" )
#     display( widgets.HBox( [ open_file, save_figures ] ), output1 )

    porder = widgets.Dropdown( options = [ ('none', 1), ('support', 2), ('class & support', 3) ], value = 2, description = 'Patterns By:', layout = {'width': 'max-content'} ) # starts with 'support'

    vorder = widgets.Dropdown( options = [ ('none', 1), ('importance', 2) ], value = 2, description = 'Variables By:', layout = {'width': 'max-content'} ) # starts with 'importance'

    coverage = widgets.FloatSlider( value = 0.0, min = 0, max = 100.0, step = 0.05, description = 'Coverage:', disabled = False, continuous_update = True, orientation = 'horizontal', readout = True, readout_format = '.2f' )
    
    range_frame = widgets.Checkbox( value = False, description = 'Range', disabled = False, indent = False )
    
    left = widgets.IntSlider( value = 450, min = 0, max = 1000, step = 5, description = 'Left:', disabled = False, continuous_update = True, orientation = 'horizontal', readout = True, readout_format = 'd' )
    
    top = widgets.IntSlider( value = 550, min = 0, max = 1000, step = 5, description = 'Top:', disabled = False, continuous_update = True, orientation = 'horizontal', readout = True, readout_format = 'd' )
    
    right = widgets.IntSlider( value = 350, min = 0, max = 1000, step = 5, description = 'Right:', disabled = False, continuous_update = True, orientation = 'horizontal', readout = True, readout_format = 'd' )
    
    bottom = widgets.IntSlider( value = 300, min = 0, max = 1000, step = 5, description = 'Bottom:', disabled = False, continuous_update = True, orientation = 'horizontal', readout = True, readout_format = 'd' )

    reset = widgets.Button( description = "Reset" )

    
    
#     display( widgets.HBox( [ porder, vorder, coverage, reset, save ] ), output )
    display( widgets.HBox( [ porder, vorder, coverage, range_frame ] ), output )
    display( widgets.HBox( [ left, right, top, bottom ] ), output )
    display( widgets.HBox( [ reset, save ] ), output )
        
    
    
    jeps_vis.display( '< JEPs >' )
    # maps_vis.display( '< MAPs >' )


    
    if file_name != None:        
        file_name_ = file_name
        jeps()

        
        
    if ( X_emb is not None ) and ( y is not None ):        
        X_emb_ = X_emb
        y_ = y
        maps()

        
    
    if ( x_name is not None ):        
        x_name_ = x_name
        tooltip_vis.display( '< >' )
        
    
    
#     open_file.on_click( open_file_f )
    porder.observe( order_filter_f2 )
    vorder.observe( order_filter_f1 )
    coverage.observe( order_filter_f2 )
    range_frame.observe( order_filter_f1 )
    left.observe( order_filter_f1 )
    right.observe( order_filter_f1 )
    top.observe( order_filter_f1 )
    bottom.observe( order_filter_f1 )
    reset.on_click( reset_f )
    save.on_click( save_figures_f )

