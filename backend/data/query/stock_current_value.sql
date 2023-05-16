with stock as (
	select i.id, i.name, sum(ji.qty) as qty_total, sum(ji.cost_total) as cost_total, i.unit
	from journal_item ji 
	left join ingredient i on ji.ingredient_id = i.id
	group by i.id, i.name, i.unit
)

select i.name, s.qty_total, i.unit, i.cost as cost_unit, s.cost_total, s.qty_total * i.cost as cost_current
from stock s
left join ingredient i on s.id = i.id
order by i.name asc;