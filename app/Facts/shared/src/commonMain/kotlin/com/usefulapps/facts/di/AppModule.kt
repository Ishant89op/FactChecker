package com.usefulapps.facts.di

import com.usefulapps.facts.data.remote.ApiService
import com.usefulapps.facts.data.remote.HTTPclient
import com.usefulapps.facts.domain.repository.CheckerRepository
import com.usefulapps.facts.viewmodel.HomeViewModel

object AppModule {
    private val httpClient = HTTPclient.create()
    private val apiService = ApiService(httpClient)
    private val repository = CheckerRepository(apiService)

    fun provideViewModel(): HomeViewModel {
        return HomeViewModel(repository)
    }
}