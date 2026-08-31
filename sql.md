# SQL Queries

Given tables:

- `tasks` (`id`, `name`, `status`, `project_id`)
- `projects` (`id`, `name`)

## 1. Get all statuses without duplicates

Get all task statuses, without repeating them, ordered alphabetically.

```sql
SELECT DISTINCT status
FROM tasks
ORDER BY status;
```

---

## 2. Count all tasks in each project

Get the count of all tasks in each project, ordered by task count descending.

```sql
SELECT
    p.id,
    p.name,
    COUNT(t.id) AS tasks_count
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id
GROUP BY p.id, p.name
ORDER BY tasks_count DESC;
```

`LEFT JOIN` is used so that projects without tasks are also included.

---

## 3. Count all tasks in each project ordered by project name

```sql
SELECT
    p.id,
    p.name,
    COUNT(t.id) AS tasks_count
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id
GROUP BY p.id, p.name
ORDER BY p.name;
```

---

## 4. Get tasks for projects whose name begins with "N"

```sql
SELECT t.*
FROM tasks t
JOIN projects p ON p.id = t.project_id
WHERE p.name LIKE 'N%';
```

---

## 5. Get projects containing the letter "a" in the middle of the name

Show the task count for each project.

There can be projects without tasks and tasks with `project_id = NULL`.

```sql
SELECT
    p.id,
    p.name,
    COUNT(t.id) AS tasks_count
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id
WHERE p.name LIKE '_%a%_'
GROUP BY p.id, p.name
ORDER BY p.name;
```

`LEFT JOIN` ensures that projects without tasks are included with a task count of `0`.

Tasks with `project_id = NULL` are not associated with any project and therefore are not counted for any project.

> If "containing the letter `a`" means that `a` can appear anywhere in the project name, use:
>
> ```sql
> WHERE p.name LIKE '%a%'
> ```

---

## 6. Get tasks with duplicate names

Get the list of tasks whose names appear more than once. Order alphabetically.

```sql
SELECT t.*
FROM tasks t
WHERE t.name IN (
    SELECT name
    FROM tasks
    GROUP BY name
    HAVING COUNT(*) > 1
)
ORDER BY t.name;
```

---

## 7. Get tasks with duplicate name and status in the "Delivery" project

Get tasks having several exact matches of both `name` and `status` from the project `Delivery`.

Order by the number of matches.

```sql
SELECT
    t.name,
    t.status,
    COUNT(*) AS matches_count
FROM tasks t
JOIN projects p ON p.id = t.project_id
WHERE p.name = 'Delivery'
GROUP BY t.name, t.status
HAVING COUNT(*) > 1
ORDER BY matches_count DESC;
```

This returns each duplicated `(name, status)` combination together with the number of times it occurs.

---

## 8. Get projects with more than 10 completed tasks

Get project names having more than 10 tasks with status `completed`.

Order by `project_id`.

```sql
SELECT
    p.id,
    p.name,
    COUNT(t.id) AS completed_tasks_count
FROM projects p
JOIN tasks t ON t.project_id = p.id
WHERE t.status = 'completed'
GROUP BY p.id, p.name
HAVING COUNT(t.id) > 10
ORDER BY p.id;
```