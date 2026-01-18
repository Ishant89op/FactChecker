package com.usefulapps.factchecker.di

import com.usefulapps.factchecker.data.remote.ApiService
import com.usefulapps.factchecker.data.remote.HTTPclient
import com.usefulapps.factchecker.domain.repository.CheckerRepository
import com.usefulapps.factchecker.viewmodel.HomeViewModel

object AppModule {
    private val httpClient = HTTPclient.create()
    private val apiService = ApiService(httpClient)
    private val repository = CheckerRepository(apiService)

    fun provideViewModel(): HomeViewModel {
        return HomeViewModel(repository)
    }
}