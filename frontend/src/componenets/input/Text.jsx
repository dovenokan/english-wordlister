import React from 'react'
import { updateCargo } from '../../redux/reducers/dataReducer';
import { useSelector,useDispatch } from "react-redux";

function Text({show}) {

    const dispatch = useDispatch()
    const { cargo } = useSelector((state) => state.wordData)

    if (show) {
        return (
            <div className="text">
                <textarea value={cargo} onChange={(e) => dispatch(updateCargo(e.target.value))} cols="60" rows="10"></textarea>
            </div>
        )
    } else {
        return (
            null
        )
    }
}

export default Text