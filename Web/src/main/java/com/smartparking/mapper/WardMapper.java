package com.smartparking.mapper;

import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.smartparking.dto.WardDTO;
import com.smartparking.entity.WardEntity;



@Component
public class WardMapper {
	@Autowired
	private ModelMapper mapper;
	
	public WardDTO toDTO(WardEntity entity) {
		WardDTO dto = mapper.map(entity, WardDTO.class);
		dto.setIdDistrict(entity.getIdDistrict());
		return dto;
	}
	
	public WardEntity toEntity(WardDTO dto) {
		WardEntity entity = mapper.map(dto, WardEntity.class);
		return entity;
	}

}
