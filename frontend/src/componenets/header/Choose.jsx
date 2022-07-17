import { options } from '../../middleware/api'
import { updateData, updateWordlistStatus, updateWordlistLoading } from '../../redux/reducers/dataReducer';
import { toggleText, toggleFile } from '../../redux/reducers/inputReducer';
import { useSelector,useDispatch } from "react-redux";

function Choose() {
    
    const dispatch = useDispatch()
    const { data, cargo } = useSelector((state) => state.wordData);

    const Generate = () => {
      let formData = new FormData();
      formData.append('text', cargo);
      options.body = formData

      dispatch(updateWordlistLoading(true))
      fetch(`${import.meta.env.VITE_BACKEND_URL}/api`, options
      ).then(
        res => res.text()
      ).then(
        data => dispatch(updateData(JSON.parse(data)))
      )
      setTimeout(() => {
        dispatch(updateWordlistStatus(true))
        dispatch(updateWordlistLoading(false))
      }, 2000);
    }

    return (
    <div className="choose">
        <div className="rounded-2xl p-4 dark:bg-gray-800 w-64 m-auto">
            <div className="w-full h-full text-center">
                <div className="flex h-full flex-col justify-between">
                    <div className="flex items-center justify-between gap-4 w-full ">
                        <button onClick={() => dispatch(toggleText())} type="button" className="py-2 px-4 bg-blue-600 hover:bg-blue-700 focus:ring-blue-500 focus:ring-offset-blue-200 text-white w-full transition ease-in duration-200 text-center text-base font-semibold shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 rounded-lg ">
                            Text
                            <br />
                            <i className="fa fa-book"></i>
                        </button>
                        <button onClick={() => dispatch(toggleFile())} type="button" className="py-2 px-4 bg-blue-600 hover:bg-blue-700 focus:ring-blue-500 focus:ring-offset-blue-200 text-white w-full transition ease-in duration-200 text-center text-base font-semibold shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 rounded-lg ">
                            File
                            <br />
                            <i className="fa fa-file"></i>
                        </button>
                        <button onClick={() => Generate()} type="button" className="py-2 px-4 bg-blue-600 hover:bg-blue-700 focus:ring-blue-500 focus:ring-offset-blue-200 text-white w-full transition ease-in duration-200 text-center text-base font-semibold shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 rounded-lg ">
                            Go!
                            <br />
                            <i className="fa fa-play"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    )
}

export default Choose