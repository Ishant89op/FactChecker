package com.usefulapps.factchecker.di

import com.usefulapps.factchecker.data.remote.ApiService
import com.usefulapps.factchecker.data.remote.HTTPclient
import com.usefulapps.factchecker.domain.repository.CheckerRepository
import com.usefulapps.factchecker.viewmodel.HomeViewModel
import org.koin.core.module.dsl.viewModel
import org.koin.dsl.module

val appModule = module {

    single { HTTPclient.create() }

    single { ApiService(get()) }

    single { CheckerRepository(get()) }

    viewModel { HomeViewModel(get()) }
}
