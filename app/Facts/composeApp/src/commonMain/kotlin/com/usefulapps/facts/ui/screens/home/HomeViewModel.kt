package com.usefulapps.facts.ui.screens.home

import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel

class HomeViewModel : ViewModel() {
    private val _input = mutableStateOf("")
    private val _inputFieldEnabled = mutableStateOf(true)
    var input = _input
    var inputFieldEnabled = _inputFieldEnabled

    private val _buttonEnabled = mutableStateOf(true)
    var buttonEnabled = _buttonEnabled

    private val _loading = mutableStateOf(false)
    var loading = _loading

    private val _result = mutableStateOf("")
    private val _showResults = mutableStateOf(false)
    var result = _result
    var showResults = _showResults

    fun setInformation(value: String) {
        _input.value = value
    }

    fun loading() {
        _loading.value = true
    }
    fun stopLoading() {
        _loading.value = false
    }

    fun showResults() {
        _showResults.value = true
    }

    fun check() {
        _inputFieldEnabled.value = false
        _buttonEnabled.value = false
        loading()
        // TODO()
        stopLoading()
        showResults()
        _inputFieldEnabled.value = true
        _buttonEnabled.value = true
    }
}