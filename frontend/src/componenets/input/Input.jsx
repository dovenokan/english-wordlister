import { useEffect } from 'react';
import File from './File'
import Text from './Text'
import { useSelector } from "react-redux";

function Input() {
  
  const { textInputStatus,fileInputStatus } = useSelector((state) => state.inputType);

  return (
    <div className="input text-black">
        <Text show={textInputStatus}/>
        <File show={fileInputStatus}/>
    </div>
  )
}

export default Input