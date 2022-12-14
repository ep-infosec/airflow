# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from __future__ import annotations

import pytest

from airflow.www import app
from tests.test_utils.config import conf_vars
from tests.test_utils.decorators import dont_initialize_flask_app_submodules


@pytest.fixture(scope="session")
def minimal_app_for_experimental_api():
    with conf_vars(
        {
            ("api", "auth_backends"): "airflow.api.auth.backend.basic_auth",
            ("api", "enable_experimental_api"): "true",
        }
    ):

        @dont_initialize_flask_app_submodules(
            skip_all_except=["init_appbuilder", "init_api_experimental", "init_api_experimental_auth"]
        )
        def factory():
            # Make sure we don't issue a warning in the test summary about deprecation
            with pytest.deprecated_call():
                return app.create_app(testing=True)  # type:ignore

        yield factory()
