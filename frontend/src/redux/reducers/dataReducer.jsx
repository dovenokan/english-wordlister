import { createSlice } from "@reduxjs/toolkit"

export const dataSlice = createSlice({
    name: "data",
    initialState: {
        data: {},
        cargo: "",
        wordlist_status: false,
        wordlist_loading: false,
    },
    reducers: {
        updateData: (state, action) => {
            state.data = action.payload
        },
        updateCargo: (state, action) => {
            state.cargo = action.payload
        },
        updateWordlistStatus: (state, action) => {
            state.wordlist_status = action.payload
        },
        updateWordlistLoading: (state, action) => {
            state.wordlist_loading = action.payload
        },
    }
}) 

export const { updateData, updateCargo, updateWordlistStatus, updateWordlistLoading } = dataSlice.actions

export default dataSlice.reducer