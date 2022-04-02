package com.parkingsmart.mapper;

import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.parkingsmart.dto.WardDTO;
import com.parkingsmart.entity.WardEntity;


@Component
public class WardMapper {
	@Autowired
	private ModelMapper mapper;
	
	public WardDTO toDTO(WardEntity entity) {
		WardDTO dto = mapper.map(entity, WardDTO.class);
		dto.setIdDistrict(entity.getDistrict().getId());
		return dto;
	}
	
	public WardEntity toEntity(WardDTO dto) {
		WardEntity entity = mapper.map(dto, WardEntity.class);
		return entity;
	}

}
