package com.usefulapps.factchecker.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.usefulapps.factchecker.data.model.Result
import com.usefulapps.factchecker.di.AppModule

@Composable
@Preview(showBackground = true, showSystemUi = true)
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
        FieldAndButtons(
            fieldEnabled = uiState.isInputEnabled,
            checkButtonEnabled = uiState.isCheckButtonEnabled,
            getInfoButtonEnabled = uiState.isGetInfoButtonEnabled,
            text = uiState.input,
            setInformation = viewModel::setInput,
            check = viewModel::check,
            getInfo = viewModel::getInfo
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
fun FieldAndButtons(
    modifier: Modifier = Modifier,
    text: String = "Write here bro!",
    fieldEnabled: Boolean = true,
    checkButtonEnabled: Boolean = true,
    getInfoButtonEnabled: Boolean = true,
    setInformation: (String) -> Unit = {},
    check: () -> Unit = {},
    getInfo: () -> Unit = {}
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

        Row(
            modifier = Modifier,
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceAround
        ) {
            Button(
                modifier = Modifier.padding(8.dp),
                onClick = check,
                enabled = checkButtonEnabled
            ) {
                Text(text = "Check")
            }

            Button(
                modifier = Modifier.padding(8.dp),
                onClick = getInfo,
                enabled = getInfoButtonEnabled
            ) {
                Text(text = "Get Info")
            }
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
    message: String = "Code Red!"
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