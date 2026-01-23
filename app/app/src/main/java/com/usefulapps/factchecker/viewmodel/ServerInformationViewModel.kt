package com.usefulapps.factchecker.viewmodel

import androidx.lifecycle.ViewModel
import com.usefulapps.factchecker.domain.repository.CheckerRepository
import com.usefulapps.factchecker.viewmodel.model.ServerInformationUiState
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class ServerInformationViewModel(
    private val repository: CheckerRepository
): ViewModel() {

    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main)

    private val _uiState = MutableStateFlow(ServerInformationUiState())
    val uiState: StateFlow<ServerInformationUiState> = _uiState

    fun testServer() {
        println("Testing API service")
        println("Launching Coroutine")
        scope.launch {
            try {
                println("Calling Repo fn")
                val service = repository.isServiceOnline()
                println("Got Output from Repo")
                _uiState.update {
                    it.copy(
                        isServerOnline = service
                    )
                }
            } catch (e: Exception) {
                println("Some error occurred")
                _uiState.update {
                    it.copy(
                        isServerOnline = false
                    )
                }
            }
        }
    }
}