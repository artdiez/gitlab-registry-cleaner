# gitlab-registry-cleaner

#### GitLab Registry Cleaner - tool for clean up the GitLab Docker registry

##### Как использовать:

* Клонировать данный репозиторий;
* Установить требуемые зависимости командой, выполняемой в корне репозитория: `pip3 install -r requirements.txt`
* В файл configs.py необходимо внести следующие измнения:
    * указать адрес вашего GitLab сервера в переменной 'gitServer';
    * указать ваш [Personal Access Token](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) в переменной 'token'.
* Для запуска необходимо в командной строке выполнить следующую команду, [передав три аргумента командной строки](https://docs.gitlab.com/ee/api/container_registry.html#delete-registry-repository-tags-in-bulk): `python3 cleaner.py <name_regex_delete> <keep_n> <older_than>`
    * name_regex_delete - регулярное выражение re2 для маски поиска тегов на удаление. Для удаления всех тегов .*;
    * keep_n - количество последних тегов, которые необходимо сохранить. Данное количество тегов будет сохранено даже в том случае, если они попадают под критерии маски и срока давности;
    * older_than - срок давности, относительно которого необходимо удалить теги. Указывается в человекочитаемом виде: 1h, 1d, 1month.

##### Пример:

Cледующая команда `python3 cleaner.py '.*' 5 1month` удалит все теги (regex '.*'), сохранив 5 последних, которые старше одного месяца.

##### Примечание:

После удаления тегов из GitLab Registry, для освобождения дискового пространства на сервере GitLab, необходимо запустить [garbage-collect](https://docs.gitlab.com/ee/administration/packages/container_registry.html#recycling-unused-tags) следующей командой: `sudo gitlab-ctl registry-garbage-collect`
