import { createSlice } from "@reduxjs/toolkit"

export const inputSlice = createSlice({
    name: "input",
    initialState: {
        textInputStatus: false,
        fileInputStatus: false,
    },
    reducers: {
        toggleText: (state, action) => {
            state.textInputStatus = action.payload
            state.fileInputStatus = false
        },
        toggleFile: (state, action) => {
            state.fileInputStatus = action.payload
            state.textInputStatus = false
        },
    }
}) 

export const { toggleText, toggleFile } = inputSlice.actions

export default inputSlice.reducer