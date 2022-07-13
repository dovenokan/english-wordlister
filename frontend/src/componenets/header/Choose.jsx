import { toggleText, toggleFile } from '../../redux/reducers/inputReducer';
import { options } from '../../middleware/api'
import { updateData, updateWordlistStatus, updateWordlistLoading } from '../../redux/reducers/dataReducer';
import { useSelector,useDispatch } from "react-redux";

function Choose() {
    
    const dispatch = useDispatch()
    const { data, cargo } = useSelector((state) => state.wordData);
  
    const formData = new FormData();
    formData.append('text', cargo);
    options.body = formData
    
    const Process = () => {
      dispatch(updateWordlistLoading(true))
      fetch("http://127.0.0.1:3434/api", options
      ).then(
        res => res.text()
      ).then(
        data => dispatch(updateData(JSON.parse(data)))
      )
      setTimeout(() => {
        dispatch(updateWordlistStatus(true))
        dispatch(updateWordlistLoading(false))
        console.log(data)
      }, 2000);
    }

    return (
    <div className="choose">
        <div className="rounded-2xl p-4 dark:bg-gray-800 w-64 m-auto">
            <div className="w-full h-full text-center">
                <div className="flex h-full flex-col justify-between">
                    <div className="flex items-center justify-between gap-4 w-full ">
                        <button onClick={() => dispatch(toggleText(true))} type="button" className="py-2 px-4 bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500 focus:ring-offset-indigo-200 text-white w-full transition ease-in duration-200 text-center text-base font-semibold shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 rounded-lg ">
                            Text
                            <br />
                            <i className="fa fa-book"></i>
                        </button>
                        <button onClick={() => dispatch(toggleFile(true))} type="button" className="py-2 px-4 bg-yellow-300 hover:bg-yellow-200 focus:ring-yellow-200 focus:ring-offset-yellow-200 text-black w-full transition ease-in duration-200 text-center text-base font-semibold shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 rounded-lg ">
                            File
                            <br />
                            <i className="fa fa-file"></i>
                        </button>
                        <button onClick={() => Process()} type="button" className="py-2 px-4 bg-green-300 hover:bg-green-200 focus:ring-green-200 focus:ring-offset-green-200 text-black w-full transition ease-in duration-200 text-center text-base font-semibold shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 rounded-lg ">
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