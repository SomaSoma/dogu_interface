# Python DoGu Interface v 1.0

## Abstract

이 문서는 [PEP 3333](https://www.python.org/dev/peps/pep-3333/)에 명시되어 있는 WSGI v1.0.1(Python Web Server Gateway Interface)를 HTTP/2의 기능 활용을 위해서 내용을 확장하였고, [WSGI 2.0 Proposal](http://wsgi.readthedocs.org/en/latest/proposals-2.0.html) 내용을 부분 적용한 표준 interface입니다.

## Specification Overview

기존 WSGI Application와의 하위호환을 위해 WSGI interface v1.0.1의 내용에서 변경된 사항은 없다. 하지만 HTTP/2에서 사용되는 ```Server Push```같은 기능을 지원하기 위해서 기존 environ에 ```dogu.push```라 이름지어진 callable object를 추가했다. 또한, client가 push를 받을 수 있는지 확인 가능한 boolean 타입의 ```dogu.push_enabled```를 추가하였다.

WSGI 2.0 제안서에 있는 내용인 CGI와의 호환성을 위해서, RFC 3875에 명시되어 있는 CGI/1.1의 CGI 환경변수를 필수적으로 지원한다. request에 대한 input stream을 담고 있는 environ의```wsgi.input```에서 ```readline(size)```함수를 지원하는 stream을 사용하도록 한다.

CGI환경변수인, SCRIPT_NAME과 PATH_INFO에는 percent encoding이라 불리는 url encoding이 적용된 원본 값을 decoding과정을 거친 값이 되고, 원본값은 RAW_PATH_INFO, RAW_SCRIPT_NAME, RAW_QUERY_STRING라는 이름으로 environ에 담는다.

## Specification Details

#### environ Variables

[PEP 3333](https://www.python.org/dev/peps/pep-3333/)에 정의되어 있는 environ의 기본적인 의미는 모두 같은 의미로 사용한다. 이 밑에는 기존 표준에 비해 차이점에 대해서만 정의한다.

| 환경변수 이름  | 의미				     |
|------------------|-----------------------------|
| `SERVER_PROTOCOL` | 만약 client의 request procotol의 버전이 HTTP/2라 한다면, 이 값은 HTTP/2.0다 |
| HTTP_ ```Variables``` | 이 변수목록에는 HTTP/2에서 정의하고 있는 가상헤더(pseudo-header)는 이에 포함되지 않는다. |
| `RAW_PATH_INFO` | decoding이 안된 PATH_INFO 이다. |
| `RAW_SCRIPT_NAME` | decoding이 안된 SCRIPT_NAME 이다. |
| `RAW_QUERY_STRING` | decoding이 안된 QUERY_STRING 이다. |
| `dogu.version` | (1, 0)의 tuple이다. |
| `dogu.push` | push할 수 있는 callable object다. HTTP/1.x 이하의  reqeust라면 호출하여도 아무반응을 하지 않고 return False를 한다. |
| SCRIPT_NAME | request의 URL에서 최종적으로 가르키고 있는 파일의 이름에 해당하는 부분으로, 없다면 빈 문자열로 처리한다.  |
| PATH_INFO | 해당하는 값이 없다면 빈 문자열로 처리한다. | 
| QUERY_STRING | 해당하는 값이 없다면 빈 문자열로 처리한다. | 
| REMOTE_ADDR | client의 IP v4주소를 갖는다. *required* |
| SERVER_SOFTWARE | 서버의 이름과 버전을 표시한다. 없다면 빈 문자열로 처리한다. |
| `dogu.push_enabled` | client가 push를 받아드릴 수 있는지에 대해서 나타내는 boolean 타입이다. HTTP/1.x 이하의 reqeust라면 False가 기본이다. |

#### _dogu.version_ tuple variable

이 값은 tuple형의 변수이며 첫번째 요소로 major 버전을 나타내고, 두번째 요소에서 minor 버전을 나타낸다. 이를 통해서 DoGu Interface의 버전에 대해서 나타내고 있고, WSGI와의 하위호환을 위해서 environ에는  _wsgi.version_ 도 tuple형으로 포함되어 있어야한다. Application은 이 값을 통해서 Server가 DoGu Interface 1.0을 지원하고 있는지 확인 할 수 있다.

#### _dogu.push_enabled_ boolean variable

HTTP/2에서는 client의 설정에 따라서 `Server Push`기능을 사용하지 않을 수 있다, 또한 client가 HTTP/1.x 이하의 버전을 사용하고 있는 유저라면 `Server Push` 기능을 지원하지 않을 것이다, 이런경우 _environ_ 에 있는 _dogu.push_enabled_ 는 False값을 갖는다. 하지만 이런 경우가 아닌 정상적으로 Server Push가 사용사능한 경우라면 True값을 갖게 된다.

#### _dogu.push_ callable object

dogu.push는 _(`push_headers`, `app`)_ 형식의 매개변수 형식을 갖고, boolean을 반환하는 callable object다. push_headers는 start_response에서 response_headers의  _(`header_name`, `header_value`)_ 형식의 tuple들이 모여 있는 list type의 변수다. HTTP/2에서 PUSH_PROMISE header에 들어갈 것이며 HTTP/2의 pseudo header들도 이 변수 안에 포함되어 있어야한다. `app`은 WSGI v 1.0.1 ([PEP 3333](https://www.python.org/dev/peps/pep-3333/))에서 정의하고 있는 environ과 start_response를 매개변수로 갖는 Application/Framework side의 callable object다. 만약 client가 HTTP/1.1로 연결했다면 Application이 _dogu.push_를 호출한다면 아무일 없이 False가 반환된다. 또한 client가 HTTP/2 유저라 하여도 `Server Push` client의 설정으로 인해서 기능이 불가능하다면 이런 경우에도 False가 반환된다. 하지만 정상적인 `Server Push`가 가능한 상황이라면 True가 반환되어, `Server Push`가 정상적으로 처리되었는지에 대해서 확인이 가능하다.

#### wsgi.input stream object

wsgi.input은 ```readline(limit=-1)```과 ```read(n=-1)```을 지원한다.

* ```readline(limit=-1)```은 stream으로 부터 한 줄을 읽어들이는 stream이고, `limit`이 설정되어 있다면 read를 할 때 `limit` 길이만큼 단위의 사이즈 만큼 읽어들인다. 한 줄의 기준은 b'\n'를 기준으로 한다.

* ```read(n=-1)```은 `n`길이만큼의 binary를 읽어오게되고, n이 음수라면 읽을 수 있는 만큼의 모든 data를 읽을 수 있다.

