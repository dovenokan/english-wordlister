import { createSlice } from "@reduxjs/toolkit"

export const inputSlice = createSlice({
    name: "input",
    initialState: {
        textInputStatus: false,
        fileInputStatus: false,
    },
    reducers: {
        toggleText: (state, action) => {
            state.textInputStatus = !state.textInputStatus
            state.fileInputStatus = false
        },
        toggleFile: (state, action) => {
            state.fileInputStatus = !state.fileInputStatus
            state.textInputStatus = false
        },
    }
}) 

export const { toggleText, toggleFile } = inputSlice.actions

export default inputSlice.reducer