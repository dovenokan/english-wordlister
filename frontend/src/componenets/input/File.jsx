import { updateCargo } from '../../redux/reducers/dataReducer';
import { useSelector,useDispatch } from "react-redux";

function File({show}) {
  
  const dispatch = useDispatch()
  const readFile = (input) => {
    let file = input.files[0];
    let reader = new FileReader();
    reader.readAsText(file);
    reader.onload = function() {
      dispatch(updateCargo(reader.result))
    };
    reader.onerror = function() {
      console.log(reader.error);
    };
}


  if (show) {
      return (
        <div className="file">
            <input 
            onChange={(e) => readFile(e.target)}
            type="file"
            />
        </div>
      )
  } else {
      return (
        null
      )
  }
}

export default File