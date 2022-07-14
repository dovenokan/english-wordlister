import { updateCargo } from '../../redux/reducers/dataReducer';
import { useSelector,useDispatch } from "react-redux";

function Text({show}) {

    const dispatch = useDispatch()
    const { cargo } = useSelector((state) => state.wordData)

    if (show) {
        return (
            <div className="text">
                <div className="flex justify-center">
                    <div className="mb-3 xl:w-96">
                        <textarea
                        value={cargo}
                        onChange={(e) => dispatch(updateCargo(e.target.value))}
                        className="
                            form-control
                            block
                            w-full
                            px-3
                            py-1.5
                            text-base
                            font-normal
                            text-gray-700
                            bg-white bg-clip-padding
                            border border-solid border-gray-300
                            rounded
                            transition
                            ease-in-out
                            m-0
                            focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none
                        "
                        id="exampleFormControlTextarea1"
                        cols="60"
                        rows="10"
                        placeholder="Your input"
                        ></textarea>
                    </div>
                </div>
            </div>
        )
    } else {
        return (
            null
        )
    }
}

export default Text