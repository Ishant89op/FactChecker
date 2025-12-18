package com.usefulapps.facts.ui.screens.home

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.usefulapps.facts.data.model.Result
import com.usefulapps.facts.di.AppModule
import com.usefulapps.facts.viewmodel.HomeViewModel
import com.usefulapps.facts.viewmodel.model.HomeUiState
import org.jetbrains.compose.ui.tooling.preview.Preview

@Composable
@Preview(showBackground = true)
fun HomeScreen(
    modifier: Modifier = Modifier
) {
    val viewModel = remember {
        AppModule.provideViewModel()
    }

    val uiState by viewModel.uiState.collectAsState()

    Column(
        modifier = modifier.padding(8.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        FieldAndButton(
            fieldEnabled = uiState.isInputEnabled,
            buttonEnabled = uiState.isButtonEnabled,
            text = uiState.input,
            setInformation = viewModel::setInput,
            check = viewModel::check
        )
        if(uiState.isLoading) Loading()
        if(uiState.showResults) {
            val errorMessage = uiState.error
            if(errorMessage != null) {
                Error(message = errorMessage)
            } else {
                Results(uiState.results)
            }
        }
    }
}

@Composable
@Preview(showBackground = true)
fun FieldAndButton(
    modifier: Modifier = Modifier,
    text: String,
    fieldEnabled: Boolean = true,
    buttonEnabled: Boolean = true,
    setInformation: (String) -> Unit,
    check: () -> Unit
) {
    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        OutlinedTextField(
            modifier = Modifier.padding(4.dp),
            value = text,
            onValueChange = setInformation,
            label = {Text("URL / Fact")},
            enabled = fieldEnabled
        )

        Button(
            modifier = Modifier.padding(8.dp),
            onClick = check,
            enabled = buttonEnabled
        ) {
            Text(text = "Check")
        }
    }
}


@Composable
@Preview(showBackground = true)
fun Loading(
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        CircularProgressIndicator()
    }
}

@Composable
@Preview(showBackground = true)
fun Error(
    modifier: Modifier = Modifier,
    message: String
) {
    Column(
        modifier = modifier
    ) {
        Text(message)
    }
}

@Composable
@Preview(showBackground = true)
fun Results(
    results: List<Result>? = null
) {
    Column(
        modifier = Modifier
    ) {
        if (results != null) {
            for(res in results) {
                Text(res.site)
                if(res.found) {
                    Text("Found!")
                    Text(res.url)
                    Text(res.snippet)
                } else {
                    Text("Not Found!")
                }
                Text(res.verdict.toString())
            }
        }
    }
}