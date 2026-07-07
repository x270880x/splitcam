#pragma once
#include <inttypes.h>

/** \file */

/*! \brief Export the function with unmangled name
 *
 * Use the EXPORT macro at the beginning of any function implementation body to 
 * add this function to the target DLL export table. The function will be 
 * exported using its unmangled name including namespace(s) in which iit is
 * defined.
 */
#define EXPORT comment(linker, "/EXPORT:" __FUNCTION__ "=" __FUNCDNAME__)

/*! \namespace splitcam::plugin
 * \brief splitcam::plugin namespace
 * 
 * It is important that all exported functions have the nested <em>splitcam::plugin::</em>
 * namespace predicate at the beginning of their names. For example, the function
 * <tt>bool init()</tt> should be exported with a name <tt>splitcam::plugin::init</tt>.
 */
namespace splitcam { namespace plugin
{
    /*! \var IPlugin_v1
     * \brief IPlugin interface identifier
	 * {A434FC43-EED2-4EAE-A792-4B92CD916FA1}
     * 
     * Depending on which version of IPlugin interface your code realizes it 
     * should return the corresponding version identifier when requested from
     * <em>::getPluginInterfaceId</em> function.
     */
	static const GUID IPlugin_v1 =
	{ 0xa434fc43, 0xeed2, 0x4eae, { 0xa7, 0x92, 0x4b, 0x92, 0xcd, 0x91, 0x6f, 0xa1 } };

    /*! \var ISource_v1
     * \brief ISource interface identifier
     * {EFEDF7CC-0795-4C38-A749-DDEA80E9DF1A}
     *
     * Depending on which version of ISource interface your code realizes it
     * should return the corresponding version identifier when requested from
     * <em>::getSourceInterfaceId()</em> function.
     */
    static const GUID ISource_v1 =
    { 0xefedf7cc, 0x795, 0x4c38, { 0xa7, 0x49, 0xdd, 0xea, 0x80, 0xe9, 0xdf, 0x1a } };


    /*! \var IImageSource_v1
     * \brief IImageSource interface identifier
	 * {D5FE39E8-2501-4D87-8379-E82AF98D2283}
     * 
     * Depending on which version of IImageSource interface your code realizes it 
     * should return the corresponding version identifier when requested from
     * <em>::getImageInterfaceId()</em> function.
     */
	static const GUID IImageSource_v1 =
	{ 0xd5fe39e8, 0x2501, 0x4d87, { 0x83, 0x79, 0xe8, 0x2a, 0xf9, 0x8d, 0x22, 0x83 } };

    /*! \var IWebSource_v1
     * \brief IWebSource interface identifier
     * {ACAF8AD1-D7B3-4B6C-A374-E79A718906F0}
     *
     * Depending on which version of IWebSource interface your code realizes it
     * should return the corresponding version identifier when requested from
     * <em>::getWebInterfaceId()</em> function.
     */
    static const GUID IWebSource_v1 =
    { 0xacaf8ad1, 0xd7b3, 0x4b6c, { 0xa3, 0x74, 0xe7, 0x9a, 0x71, 0x89, 0x6, 0xf0 } };


    /*! \var IEventHandler_v1
     * \brief IEventHandler interface identifier
	 * {7442FD68-30F1-4D19-97C2-8003014468FD}
     * 
     * Depending on which version of IEventHandler interface your code realizes it 
     * should return the corresponding version identifier when requested from
     * <em>::getEventsInterfaceId</em> function.
     */
	static const GUID IEventHandler_v1 =
	{ 0x7442fd68, 0x30f1, 0x4d19, { 0x97, 0xc2, 0x80, 0x3, 0x1, 0x44, 0x68, 0xfd } };

    /*! Possible plugin types supported by SplitCam
     *
     * If your plugin provides an image or video to be added to SplitCam user 
     * interface it should return <em>imageSource</em> from <em>::getType()</em>
     * function. And it should implement and export <em>IImageSource</em>
     * function set.
     */
	enum class PluginType
	{
		undefined,
		imageSource,
        webSource,
		imageProcessor,
		audioSource
	};

    /*! Plugin implementation version
     *
     * Plugin developers define the privately used plugin version using their 
     * own versioning system. This value is not currently used by SplitCam.
     */
	struct Version
	{
		uint8_t major;
		uint8_t minor;
		uint8_t build;
	};

    /*! The format of images provided by this plugin
     *
     * Currently only two image formats are supported: opaque RGB24, and 
     * transparent or semitransparent RGBA format.
     */
	enum class ImageFormat
	{
		imageRGB24,
		imageRGBA
	};

    /*! Helper pure virtual class defining which function set must be implemented 
     * in this interface.
    */
	class IPlugin
	{
	public:
        /*!
         * A wrapper around exported <em>::getPluginInterfaceId()</em> function
         */
		virtual GUID iid() const = 0;

        /*!
         * A wrapper around exported <em>::getPluginId()</em> function
         */
		virtual const wchar_t* getId() const = 0;

        /*!
         * A wrapper around exported <em>::getPluginName()</em> function
         */
		virtual const wchar_t* getName() const = 0;

        /*!
         * A wrapper around exported <em>::getPluginProvider()</em> function
         */
		virtual const wchar_t* getProvider() const = 0;

        /*!
         * A wrapper around exported <em>::getPluginVersion()</em> function
         */
		virtual Version getVersion() const = 0;

        /*!
         * A wrapper around exported <em>::getType()</em> function
         */
		virtual PluginType getType() const = 0;

        /*!
         * A wrapper around exported <em>::init()</em> function
         */
		virtual bool init() = 0;

        /*!
         * A wrapper around exported <em>::release()</em> function
         */
		virtual void release() = 0;
	};

    /*! Helper pure virtual class defining which function set must be implemented
     * in this interface.
    */
    class ISource
    {
    public:

        /*!
         * A wrapper around exported <em>::getSourceInterfaceId()</em> function
         */
        virtual GUID iid() const = 0;

        /*!
         * A wrapper around exported <em>::getSourceName()</em> function
         */
        virtual const wchar_t* getName() const = 0;

        /*!
         * A wrapper around exported <em>::getSourceSize(size_t&, size_t&)</em> function
         */
        virtual void getSize(size_t&, size_t&) const = 0;

        /*!
         * A wrapper around exported <em>::setCanvasSize(size_t, size_t)</em> function
         */
        virtual void setCanvasSize(size_t, size_t) = 0;

        /*!
         * A wrapper around exported <em>::openSource(const wchar_t*)</em> function
         */
        virtual void open(const wchar_t*) = 0;

        /*!
         * A wrapper around exported <em>::closeSource(const wchar_t*)</em> function
         */
        virtual void close(const wchar_t*) = 0;

        /*!
         * A wrapper around exported <em>::pauseSource(const wchar_t*, bool)</em> function
         */
        virtual void pause(const wchar_t*, bool) = 0;
    };

    /*! Helper pure virtual class defining which function set must be implemented
     * in this interface.
    */
	class IImageSource
	{
	public:
        /*! \typedef DataCallback
         * Image source callback function used to update the image currently 
         * presented to the program user.
         * 
         * @param srcId The string identifier of the source whose image should be updated
         * @param format Image format as one of <em>ImageFormat</em> values
         * @param data Pointer to actual data of the image
         * @param width Width of the image in pixels
         * @param height Height of the image in pixels
         * @param param SplitCam parameter provided in with a call to <em>IImageSource::setDataCallback</em> function
         */
		using DataCallback = void(__stdcall*)(const wchar_t* srcId, ImageFormat format, const uint8_t* data, const size_t width, const size_t height, void* param);

        /*!
         * A wrapper around exported <em>::getImageInterfaceId()</em> function
         */
        virtual GUID iid() const = 0;

        /*!
         * A wrapper around exported <em>::getImageFormat()</em> function
         */
		virtual ImageFormat getFormat() const = 0;
        
        /*!
         * A wrapper around exported <em>::setDataCallback(splitcam::plugin::IImageSource::DataCallback, void*)</em> function
         */
		virtual void setDataCallback(DataCallback function, void* param) = 0;

	};

    /*! Helper pure virtual class defining which function set must be implemented
     * in this interface.
    */
    class IWebSource
    {
    public:

        /*!
         * A wrapper around exported <em>::getWebInterfaceId()</em> function
         */
        virtual GUID iid() const = 0;

        /*!
         * A wrapper around exported <em>::getWebUrl()</em> function
         */
        virtual const wchar_t* getUrl() const = 0;

    };

    /*! Helper pure virtual class defining which function set must be implemented
     * in this interface.
    */
	class IEventHandler
	{
	public:

        /*!
         * A wrapper around exported <em>::getEventsInterfaceId()</em> function
         */
		virtual GUID iid() const = 0;

        /*!
         * A wrapper around exported <em>::onLoad()</em> function
         */
		virtual void onLoad() = 0;

        /*!
         * A wrapper around exported <em>::onUnload()</em> function
         */
		virtual void onUnload() = 0;

        /*!
         * A wrapper around exported <em>::onCanvasSize(size_t, size_t)</em> function
         */
		virtual void onCanvasSize(size_t, size_t) = 0;

        /*!
         * A wrapper around exported <em>::onPosition(const wchar_t*, int, int, size_t, size_t)</em> function
         */
		virtual void onPosition(const wchar_t*, int, int, size_t, size_t) = 0;

	};

    /*! \defgroup Exports
     * Exported functions by logical groups */
    /*! @{ */

    /*! \defgroup Plugin 
     * Common to every plugin */
    /*! @{ */

	////////////////////////////////////////////////////////////////////////////////////
	// << exports >>
	// IPlugin

    /*!
     * SplitCam calls this function to get the plugin interface identifier. 
     * The interface identifier defines the function set supported by the 
     * current plugin module.
     * \return GUID of the supported plugin interface version
     */
	const GUID getPluginInterfaceId();

    /*!
     * This function provides SplitCam with a unique identifier of the current
     * plugin. The plugin identifier is used to distinguish this plugin from 
     * other plugins loaded by SplitCam.
     * \return A plugin developer assigned unique identifier
     */
	const wchar_t* getPluginId();

    /*!
     * Plugin name will be used in SplitCam user interface as a display element
     * for this plugin instance. This name is how user sees your plugin.
     * \return Human readable name of the plugin
     */
	const wchar_t* getPluginName();

    /*!
     * Provides SplitCam with a name of plugin developer. This may be your 
     * company name or trademark. The plugin developer decides what this 
     * value really presents.
     * \return Human readable name of plugin developer
     */
	const wchar_t* getPluginProvider();

    /*!
     * Current version of the plugin as defined by plugin developer. If several
     * plugins having the same ID are available to end user SplitCam may choose 
     * the one having the greatest version and ignore other plugins with the 
     * same ID. The plugin ID is returned by <em>::getPluginId</em> function.
     * \return Plugin version structure as <em>splitcam::plugin::Version</em>
     */
	const splitcam::plugin::Version getPluginVersion();

    /*!
     * Currently only one plugin type is supported by SplitCam: image source.
     * This plugin type can provide SplitCam with a source of still images or
     * videos. The plugin developer decides how often the image is updated. To
     * update the image you call <em>IImageSource::DataCallback</em>
     * callback function.
     *
     * More plugin types will be added to future versions of SplitCam.
     * \return plugin type as <em>splitcam::plugin::PluginType</em>
     */
	splitcam::plugin::PluginType getType();

    /*!
     * SplitCam calls <em>init()</em> function to give the plugin a chance to
     * initialize itself. The <em>init()</em> is called only if the plugin is 
     * recognized and required function sets are verified by SplitCam. If this 
     * function returns <em>false</em> then the plugin will be unloaded and not 
     * used by SplitCam.
     * 
     * \return Boolean value indicating success or failure during initialization
     */
	bool init();

    /*!
     * SplitCam calls <em>release()</em> to notify the plugin that it should
     * prepare itself for being unloaded. Any resources should be freed and any
     * plugin specific operations related to plugin unloading should be 
     * performed inside this function.
     * 
     */
	void release();

    /*! @} */
    
    /*! \defgroup EventHandler
     * Required event handlers */
    /*! @{ */


    ////////////////////////////////////////////////////////////////////////////////////
	// << exports >>
	// IEventHandler

    /*!
     * SplitCam calls this function to get the events interface identifier. 
     * The interface identifier defines the function set supported by the 
     * current plugin module.
     * \return GUID of the supported events interface version
     */
	const GUID getEventsInterfaceId();
    
    /*!
     * SplitCam calls this function as soon as the plugin module is loaded.
     *
     * This function call will be followed by <em>::init()</em> function call
     * if this plugin is recognized and the function sets are verified by SplitCam.
     */
	void onLoad();

    /*!
     * SplitCam calls this function to notify the plugin that the module is 
     * about to be unloaded.
     *
     * This function call always follows the <em>::release()</em> function call.
     */
	void onUnload();

    /*!
     * SplitCam calls this function to notify the plugin of the canvas size change
     * initiated by the program user.
     *
     * @param width New canvas width in pixels
     * @param height New canvas height in pixels
     */
	void onCanvasSize(size_t width, size_t height);

    /*!
     * SplitCam calls this function every time the plugin layer size or position 
     * is changed. 
     *
     * @param srcId Source instance identifier
     * @param x New layer horizontal position in pixels relative to canvas (may be negative)
     * @param x New layer vertical position in pixels relative to canvas (may be negative)
     * @param width New layer width in pixels
     * @param height New layer height in pixels
     */
	void onPosition(const wchar_t* srcId, int x, int y, size_t width, size_t height);

    /*! @} */

    /*! \defgroup ISource
    * Required by every source provider */
    /*! @{ */

    ////////////////////////////////////////////////////////////////////////////////////
    // << exports >>
    // ISource

    /*!
    * SplitCam calls this function to get the source interface identifier.
    * The interface identifier defines the function set supported by the
    * current plugin module.
    * \return GUID of the supported source interface version
    */
    const GUID getSourceInterfaceId();

    /*!
     * Source name will be used in SplitCam user interface as a display name
     * for this source element. This name is how user sees your source.
     * \return Human readable name of the source
     */
    const wchar_t* getSourceName();

    /*!
     * SplitCam calls this function to get the original size of the source in pixels.
     * The original size may be used to proportionally resize the layer, for example.
     *
     * @param width Original source width in pixels
     * @param height Original source height in pixels
     */
    void getSourceSize(size_t& width, size_t& height);

    /*!
     * SplitCam notifies the source about the canvas size as soon as the source
     * is created. Please note that the canvas size may change during the lifetime
     * of the source. If the canvas size changes the plugin will be notified about the
     * change with this function.
     *
     * @param width Current canvas width
     * @param height Current canvas height
     */
    void setCanvasSize(size_t width, size_t height);

    /*!
     * Create a new image source instance and assign the identifier to it. This
     * identifier will be used in future calls to other source management functions.
     * This identifier is also used in a call to <em>IImageSource::DataCallback</em>
     * as the first parameter of the function.
     *
     * Source identifier is required because user can create more than one instance
     * of the source on the same scene or she can create multiple instances of
     * the image source on different scenes. Each image source can provide its
     * own image or all of the can provide the same image in all instances. It
     * up to plugin developer to define the exact behaviour.
     *
     * @param srcId The source identifier assigned to newly created instance
     */
    void openSource(const wchar_t* srcId);

    /*!
     * Notifies the plugin that the user have chosen to delete the source from
     * the scene or the program is exiting. You should free up all resources
     * used by this source instance and the srcId becomes invalid in this
     * session unless it is assigned to a new source instance in the
     * <em>::openSource</em> function call.
     *
     * @param srcId The source instance identifier
     */
    void closeSource(const wchar_t* srcId);

    /*!
     * The user paused the source, made it invisible or switched to another scene.
     * The source should not be deleted but it is required to lower down resource
     * usage to a minimum. Ideally the resource instance should not consume any
     * CPU at all in paused state and it should free up all not immediately required
     * memory resources.
     *
     * @param srcId The source instance identifier
     */
    void pauseSource(const wchar_t* srcId, bool val);

    /*! @} */

    /*! \defgroup ImageSource
     * Required by every image source provider */
    /*! @{ */

	////////////////////////////////////////////////////////////////////////////////////
	// << exports >>
	// IImageSource

    /*!
     * SplitCam calls this function to get the image source interface identifier. 
     * The interface identifier defines the function set supported by the 
     * current plugin module.
     * \return GUID of the supported events interface version
     */
	const GUID getImageInterfaceId();

    /*!
     * SplitCam uses this function to request the image format provided by this 
     * image source interface.
     * 
     * \return Image format as one of <em>ImageFormat</em> values
     */
	splitcam::plugin::ImageFormat getImageFormat();

    /*!
     * SplitCam calls this function to set the callback used for passing images
     * from the plugin back to SplitCam. Every time this function is called the
     * image displayed on the screen by this plugin will be updated with a new 
     * one. It is important to pass the <tt>param</tt> parameter unchanged in 
     * every call to the callback function.
     * 
     * @param cb Callback function to update the source instance image
     * @param param SplitCam set parameter that must be passed back unchanged in a call to callback function
     */
	void setDataCallback(splitcam::plugin::IImageSource::DataCallback cb, void* param);

    /*! @} */

    /*! \defgroup WebSource
     * Required by every web source provider */
    /*! @{ */

     ////////////////////////////////////////////////////////////////////////////////////
     // << exports >>
     // IWebSource

    /*!
     * SplitCam calls this function to get the web source interface identifier.
     * The interface identifier defines the function set supported by the
     * current plugin module.
     * \return GUID of the supported events interface version
     */
    const GUID getWebInterfaceId();

    /*!
     * SplitCam uses this function to request the URL of a web page that should be 
     * opened in the web browser associated with the current web source instance.
     *
     * \return URL address of a web resource to be opened in the pbrowser
     */
    const wchar_t* getWebUrl();

    /*! @} */
    /*! @} */
}}
