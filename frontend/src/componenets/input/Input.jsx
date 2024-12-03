import { useEffect } from 'react';
import File from './File'
import Text from './Text'
import { useSelector, useDispatch } from "react-redux";
import { toggleText, toggleFile } from '../../redux/reducers/inputReducer';
import { updateData, updateWordlistStatus, updateWordlistLoading } from '../../redux/reducers/dataReducer';
import { options } from '../../middleware/api';

function Input() {
  const dispatch = useDispatch();
  const { textInputStatus, fileInputStatus } = useSelector((state) => state.inputType);
  const { cargo } = useSelector((state) => state.wordData);

  const Generate = () => {
    let formData = new FormData();
    formData.append('text', cargo);
    options.body = formData;

    dispatch(updateWordlistLoading(true));
    fetch(`${import.meta.env.VITE_BACKEND_URL}/api`, options)
      .then(res => res.text())
      .then(data => dispatch(updateData(JSON.parse(data))))
      .finally(() => {
        dispatch(updateWordlistStatus(true));
        dispatch(updateWordlistLoading(false));
      });
  };

  return (
    <div className="input-section full-width">
      <div className="input-container full-width">
        <Text show={textInputStatus}/>
        <File show={fileInputStatus}/>
      </div>
      <div className="input-controls full-width">
        <button 
          className={`control-btn full-width ${textInputStatus ? 'active' : ''}`}
          onClick={() => dispatch(toggleText())}
        >
          <i className="fa fa-keyboard-o"></i>
          Text Input
        </button>
        <button 
          className={`control-btn full-width ${fileInputStatus ? 'active' : ''}`}
          onClick={() => dispatch(toggleFile())}
        >
          <i className="fa fa-file-text-o"></i>
          File Upload
        </button>
        <button 
          className="control-btn full-width"
          onClick={Generate}
        >
          <i className="fa fa-play"></i>
          Generate
        </button>
      </div>
    </div>
  )
}

export default Input