import { configureStore } from "@reduxjs/toolkit";
import inputReducer from "./reducers/inputReducer";
import dataReducer from "./reducers/dataReducer";

const store = configureStore({
  reducer: {
    inputType: inputReducer,
    wordData: dataReducer,
  },
})

export default store