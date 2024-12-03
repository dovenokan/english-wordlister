import { updateCargo } from '../../redux/reducers/dataReducer';
import { useSelector, useDispatch } from "react-redux";
import { useEffect } from 'react';

function Text({show}) {
    const dispatch = useDispatch();
    const { cargo } = useSelector((state) => state.wordData);

    // Clear results when input is empty
    useEffect(() => {
        if (!cargo.trim()) {
            dispatch(updateCargo(''));
        }
    }, [cargo, dispatch]);

    // Debounce input to prevent excessive updates
    const handleInputChange = (e) => {
        const value = e.target.value;
        dispatch(updateCargo(value));
    };

    if (show) {
        return (
            <div className="text-input-wrapper">
                <textarea
                    value={cargo}
                    onChange={handleInputChange}
                    className="text-input"
                    placeholder="Enter text to analyze..."
                    spellCheck="false"
                />
                <div className="text-controls">
                    <button 
                        className="clear-btn"
                        onClick={() => dispatch(updateCargo(''))}
                        disabled={!cargo}
                    >
                        <i className="fa fa-times"></i>
                    </button>
                </div>
            </div>
        )
    }
    return null;
}

export default Text