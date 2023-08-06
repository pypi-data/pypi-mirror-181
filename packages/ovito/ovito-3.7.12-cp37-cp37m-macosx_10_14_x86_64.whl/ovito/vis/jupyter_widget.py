import numpy
import ovito
from ovito.vis import Viewport

try:
    # Try to import the ipywidgets module and catch the ImportError if it is not installed in the local environment.  
    import ipywidgets
    from traitlets import Unicode, Int, Float, Bool, Tuple, List, Dict, Instance, observe
    from .jupyter_traits import Array, array_shape
    from contextlib import contextmanager
    import IPython.display

    @ipywidgets.register
    class JupyterViewportWidget(ipywidgets.DOMWidget):

        # Name of the widget view class in the front-end.
        _view_name = Unicode('OvitoViewportView').tag(sync=True)

        # Name of the widget model class in the front-end.
        _model_name = Unicode('OvitoViewportModel').tag(sync=True)

        # Name of the front-end module containing the widget view.
        _view_module = Unicode('jupyter-ovito').tag(sync=True)

        # Name of the front-end module containing the widget model.
        _model_module = Unicode('jupyter-ovito').tag(sync=True)

        # Version of the front-end module containing the widget view.
        _view_module_version = Unicode('^0.1.4').tag(sync=True)
        # Version of the front-end module containing the widget model.
        _model_module_version = Unicode('^0.1.4').tag(sync=True)

        antialiasing = Bool(False).tag(sync=True)
        enable_vr = Bool(False).tag(sync=True)
        vr_scale = Float(1.0).tag(sync=True)

        # The viewport camera parameters.
        camera_params = Dict(per_key_traits={
            'fov': Float(),
            'perspective': Bool(),
            'matrix': List(minlen=3, maxlen=3, trait=List(minlen=4, maxlen=4, trait=Float())),
            'up': Tuple(Float(), Float(), Float()),
        }, allow_none=True).tag(sync=True)

        # Flags that suppress handling of change notifications for the camera trait.
        _ignore_camera_notifications = Bool(False)

        # The point in space around which the camera orbits. 
        orbit_center = Tuple(Float(), Float(), Float(), default_value=(0.0, 0.0, 0.0)).tag(sync=True)

        # The current scene graph.
        scene = Dict().tag(sync=True)

        # The viewport displayed by this widget.
        viewport = Instance(Viewport, allow_none=True)

        # The special scene renderer managed by this widget.
        scene_renderer = Instance(ovito.nonpublic.SceneGraphRenderer, args=())

        debug_view = ipywidgets.Output(layout={'border': '1px solid red'})

        def __init__(self, *args, **kwargs):
            super(JupyterViewportWidget, self).__init__(*args, **kwargs)
            self.on_msg(self._handle_frontend_event)
            self.refresh()

        @observe('viewport')
        def _on_viewport_changed(self, change):
            self.orbit_center = self.viewport.orbit_center if self.viewport else (0.0, 0.0, 0.0)
            self.send_camera()
            pass

        @contextmanager
        def _suppress_camera_notifications(self):
            self._ignore_camera_notifications = True
            try: yield
            finally: self._ignore_camera_notifications = False

        @debug_view.capture()
        def send_camera(self):
            with self._suppress_camera_notifications():
                self.camera_params = {
                    'fov': self.viewport.fov,
                    'perspective': self.viewport.is_perspective_projection,
                    'matrix': self.viewport.camera_tm.tolist(),
                    'up': tuple(self.viewport.camera_up),
                } if self.viewport else None

        @observe('camera_params')
        @debug_view.capture()
        def receive_camera(self, change):
            if self._ignore_camera_notifications:
                return
            if self.viewport and self.camera_params:
                if self.camera_params['perspective'] != self.viewport.is_perspective_projection:
                    self.viewport.type = Viewport.Type.Perspective if self.camera_params['perspective'] else Viewport.Type.Ortho
                self.viewport.fov = self.camera_params['fov']
                self.viewport.camera_tm = self.camera_params['matrix']
                self.viewport.camera_up = self.camera_params['up']

        @debug_view.capture()
        def _handle_frontend_event(self, _, content, buffers):
            #event_type = content.get("event", None)
            print("Received unknown custom message from front-end:", content)

        def refresh(self):
            if not self.viewport:
                return
            self.orbit_center = self.viewport.orbit_center
            self.scene = self.scene_renderer.capture_frame(self.viewport)

    # Implementation of the Viewport.create_jupyter_widget() method:
    def _Viewport_create_jupyter_widget_implementation(self, **kwargs):
        if not 'layout' in kwargs:
            kwargs['layout'] = ipywidgets.Layout(width='400px', height='200px')
        return JupyterViewportWidget(viewport=self, **kwargs)

    # Implementation of the Viewport._ipython_display_() special method.
    # See https://ipython.readthedocs.io/en/stable/config/integrating.html#integrating-your-objects-with-ipython
    def _Viewport_ipython_display_(self):
        IPython.display.display(self.create_jupyter_widget())
    Viewport._ipython_display_ = _Viewport_ipython_display_

except ImportError:
    # Swallow import failure in case the ipywidgets module is not installed.
    def _Viewport_create_jupyter_widget_implementation(self, **kwargs):
        import warnings
        warnings.warn("Cannot create Jupyter widget, because the Python package 'ipywidgets' is not installed. "
            "Please install the 'ipywidgets' package in your Python interpreter if you want to use the Viewport.create_jupyter_widget() "
            "method in Jupyter notebooks. Restart the kernel to reload the ovito package.", stacklevel=1)
        return None

# Implementation of the Viewport.create_jupyter_widget() method:
def _Viewport_create_jupyter_widget(self, **kwargs):
    """
    create_jupyter_widget(**kwargs) -> ipywidgets.DOMWidget

    Creates an interactive widget to be embedded in Jupyter notebooks, which displays the 3d scene as seen through this virtual viewport.
    The method returns an interactive notebook element, which accepts mouse inputs similar to the viewport windows 
    of the OVITO desktop application. It may be necessary to call :func:`display <ipython:IPython.display.display>` in order to show the widget:

    .. code-block::

        vp = Viewport(type=Viewport.Type.Perspective, camera_dir=(0.5, 1.0, -0.4))
        vp.zoom_all()
        widget = vp.create_jupyter_widget()
        display(widget)

    The `Jupyter widget <https://ipywidgets.readthedocs.io/en/stable/>`__ returned by this method is permanently linked to this :py:class:`Viewport` instance. 
    Any changes you subsequently make to the non-visual :py:class:`Viewport`, for example, setting its :py:attr:`camera_pos` or :py:attr:`camera_dir`, will be 
    reflected by the visual viewport widget. Vice versa do all user interactions with the viewport widget
    update the corresponding fields of the :py:class:`!Viewport` object.

    .. important::

        This method requires the `ipywidgets <https://ipywidgets.readthedocs.io/en/stable/user_install.html>`__ Python package.
        Please install this package in the Python interpreter used by your Jupyter environment.

    The :py:meth:`create_jupyter_widget` method forwards keyword arguments to the widget's constructor.
    This lets you specify the ``layout`` attribute `controlling the size of the widget <https://ipywidgets.readthedocs.io/en/stable/examples/Widget%20Layout.html>`__:

    .. code-block::

        widget = vp.create_jupyter_widget(layout = ipywidgets.Layout(width='500px', height='400px'))
    
    .. caution::

        This method is still under active development and not fully functional yet. Expect these known limitations:

            * Changes you make to the scene or the viewport camera do not automatically trigger a refresh of the viewport widget.
              You need to explicitly call ``widget.refresh()`` to update the widget display whenever you change the scene.
            * Semi-transparent objects will likely be rendered incorrectly.
            * Viewport layers are not supported yet.
            * Object picking with the mouse is not supported yet.
            * Widget is compatible with JupyterLab but may not work in other notebook interfaces yet.

        These limitations will be resolved in a future update of the OVITO Python module.
        Please support the development of this new feature and report any issues you may encounter in our `issue tracker <https://gitlab.com/stuko/ovito/-/issues>`__
        or in the `OVITO forum <https://www.ovito.org/forum/>`__. 

    .. versionadded:: 3.7.9

    """        
    return _Viewport_create_jupyter_widget_implementation(self, **kwargs)
Viewport.create_jupyter_widget = _Viewport_create_jupyter_widget
